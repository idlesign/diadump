import os
import io
from setuptools import setup, find_packages

from diadump import VERSION


PATH_BASE = os.path.dirname(__file__)


def get_readme():
    # This will return README (including those with Unicode symbols).
    with io.open(os.path.join(PATH_BASE, 'README.rst')) as f:
        return f.read()


setup(
    name='diadump',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/diadump',

    description='Filmstrip dumper',
    long_description=get_readme(),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[],
    setup_requires=[
        'click',
        'requests',
        'beautifulsoup4',
    ],

    entry_points={
        'console_scripts': ['diadump = diadump.cli:main'],
    },

    test_suite='tests',

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License'
    ],
)


