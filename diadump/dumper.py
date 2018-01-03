import logging
import re
from os import path, makedirs

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

RE_IMAGE_COMMENT = re.compile('<!--dle_image_begin:([^|]+)|-->')


def configure_logging(level=None, format=None):
    logging.basicConfig(level=level or logging.INFO, format=format or '%(message)s')


def get_data(url, stream=False):
    headers = {
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.106 Safari/537.36',
    }
    response = requests.get(url, allow_redirects=True, timeout=3, headers=headers, stream=stream)

    if stream:
        return response

    return response.text


def make_soup(html):
    return BeautifulSoup(html, 'lxml')


def extract_titles(soup):
    LOGGER.debug('Extracting titles ...')

    titles = soup.select('.news2 h3 a')

    for title in titles:
        yield title['href'], title.text.strip()


def get_next_page_url(soup):
    next_page_url = soup.select('.nextprev a')

    try:
        next_page_url = next_page_url[0]['href']

    except IndexError:
        return None

    return next_page_url


def extract_images(html, target_dir, force=False):
    LOGGER.debug('Extracting images ...')

    images_urls = []

    for image_url in RE_IMAGE_COMMENT.findall(html):
        image_url = image_url.strip()
        image_url and images_urls.append(image_url)

    total = len(images_urls)

    for idx, image_url in enumerate(images_urls, 1):
        LOGGER.info('Image [%s/%s] ...', idx, total)

        target_fname = path.basename(image_url)
        target_fname = str(idx).zfill(3) + path.splitext(target_fname)[1]
        target_fname = path.join(target_dir, target_fname)

        if not path.exists(target_fname) or force:

            LOGGER.debug('Saving into %s ...', target_fname)

            response = get_data(image_url, stream=True)

            with open(target_fname, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            LOGGER.debug('Image already exists. Skipped')


def walk_pages(url, page_num=0):
    LOGGER.info('Page %s ...', url)

    soup = make_soup(get_data(url))

    yield from extract_titles(soup)

    next_url = get_next_page_url(soup)
    LOGGER.debug('Next URL is: %s', next_url)

    if next_url:
        yield from walk_pages(next_url, page_num+1)


def build_title_dir(target_dir, item_title, force=False):
    title_dir = path.join(target_dir, item_title)

    if not path.exists(title_dir) or force:
        return title_dir

    else:
        LOGGER.debug('Title directory already exists. Skipped')


def dump_one(url, target_dir, force=False):
    html = get_data(url)
    soup = make_soup(html)
    item_title = soup.select('#news-title')[0].text

    LOGGER.info('Processing `%s` ...', item_title)

    title_dir = build_title_dir(target_dir, item_title)

    if title_dir:
        makedirs(title_dir, exist_ok=True)
        extract_images(html, title_dir, force=force)


def dump_many(url, target_dir, max_titles=float('inf'), force=False):
    titles_urls = []

    for idx, (title_url, title_header) in enumerate(walk_pages(url), 1):

        if build_title_dir(target_dir, title_header, force=force):
            titles_urls.append(title_url)

        else:
            LOGGER.info('Skipping `%s` ...', title_header)

        if idx == max_titles:
            break

    total = len(titles_urls)

    for idx, title_url in enumerate(titles_urls, 1):
        LOGGER.info('Title [%s/%s] ...', idx, total)
        dump_one(title_url, target_dir, force=force)
