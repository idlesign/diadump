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
        yield title['href']


def get_next_page_url(soup):
    next_page_url = soup.select('.nextprev a')

    try:
        next_page_url = next_page_url[0]['href']

    except IndexError:
        return None

    return next_page_url


def extract_images(html, target_dir):
    LOGGER.debug('Extracting images ...')

    images_urls = RE_IMAGE_COMMENT.findall(html)

    idx = 0

    for image_url in images_urls:
        image_url = image_url.strip()
        if not image_url:
            continue

        idx += 1

        target_fname = path.basename(image_url)
        target_fname = str(idx).zfill(3) + path.splitext(target_fname)[1]
        target_fname = path.join(target_dir, target_fname)

        LOGGER.debug('Saving into %s ...', target_fname)

        response = get_data(image_url, stream=True)

        with open(target_fname, 'wb') as f:
            for chunk in response.iter_content():
                f.write(chunk)


def walk_pages(url):
    LOGGER.debug('Fetching %s ...', url)

    soup = make_soup(get_data(url))

    yield from extract_titles(soup)

    next_url = get_next_page_url(soup)
    LOGGER.debug('Next URL is: %s', next_url)

    if next_url:
        yield from walk_pages(next_url)


def dump_one(url, target_dir):
    html = get_data(url)
    soup = make_soup(html)
    item_title = soup.select('#news-title')[0].text

    LOGGER.info('Dumping %s ...', item_title)

    title_dir = path.join(target_dir, item_title)

    makedirs(title_dir, exist_ok=True)
    extract_images(html, title_dir)


def dump_many(url, target_dir, max_titles=float('inf')):
    for idx, item_url in enumerate(walk_pages(url), 1):

        dump_one(item_url, target_dir)

        if idx == max_titles:
            break
