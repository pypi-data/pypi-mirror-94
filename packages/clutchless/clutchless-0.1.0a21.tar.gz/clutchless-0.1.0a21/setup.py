# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutchless',
 'clutchless.command',
 'clutchless.command.prune',
 'clutchless.domain',
 'clutchless.entrypoints',
 'clutchless.external',
 'clutchless.service',
 'clutchless.spec',
 'clutchless.spec.prune']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'docopt>=0.6.2,<0.7.0',
 'texttable>=1.6.3,<2.0.0',
 'torrentool>=1.1.0,<2.0.0',
 'transmission-clutch>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['clutchless = clutchless.entrypoints.cli:main']}

setup_kwargs = {
    'name': 'clutchless',
    'version': '0.1.0a21',
    'description': 'A CLI tool to manage torrents and their data in Transmission',
    'long_description': "Clutchless\n----------\n\n.. image:: https://img.shields.io/pypi/v/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI badge\n\n.. image:: https://img.shields.io/pypi/pyversions/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI versions badge\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Black formatter badge\n\n.. image:: https://img.shields.io/pypi/l/clutchless.svg\n    :target: https://en.wikipedia.org/wiki/MIT_License\n    :alt: License badge\n\n.. image:: https://img.shields.io/pypi/dm/clutchless.svg\n    :target: https://pypistats.org/packages/clutchless\n    :alt: PyPI downloads badge\n\n.. image:: https://coveralls.io/repos/github/mhadam/clutchless/badge.svg?branch=develop\n    :target: https://coveralls.io/github/mhadam/clutchless?branch=develop\n\nOther links\n===========\n\n* `Developer documentation`_\n\nSupport\n=======\n\nbtc: bc1q9spjh7nuqatz4pa7dscd0357p3ql588tla6af7\n\nQuick start\n===========\n\nInstall the package:\n\n.. code-block:: console\n\n    $ pip install clutchless\n\nThe ``-h`` flag can be used to bring up documentation, e.g. ``clutchless -h``::\n\n    A tool for working with torrents and their data in the Transmission BitTorrent client.\n\n    Usage:\n        clutchless [options] [-v ...] <command> [<args> ...]\n\n    Options:\n        -a <address>, --address <address>   Address for Transmission (default is http://localhost:9091/transmission/rpc).\n        -h, --help  Show this screen.\n        -v, --verbose   Verbose terminal output (multiple -v increase verbosity).\n\n    The available clutchless commands are:\n        add         Add metainfo files to Transmission (with or without data).\n        find        Locate data that belongs to metainfo files.\n        link        For torrents with missing data in Transmission, find the data and set the location.\n        archive     Copy metainfo files from Transmission for backup.\n        organize    Migrate torrents to a new location, sorting them into separate folders for each tracker.\n        prune       Clean up things in different contexts (files, torrents, etc.).\n        dedupe      Delete duplicate metainfo files from paths.\n\n    See 'clutchless help <command>' for more information on a specific command.\n\nExamples\n========\n\nTo copy all the metainfo files (``.torrent``) in Transmission to ``~/torrent_archive``::\n\n    clutchless archive ~/torrent_archive\n\n\nTo add some torrents to Transmission, searching ``~/torrent_archive`` for metainfo files and finding data in\n``~/torrent_data``::\n\n    clutchless add ~/torrent_archive -d ~/torrent_data\n\nTo look for matching data given a search folder (``~/torrent_data``) and a directory (``~/torrent_files``)\nthat contains metainfo files::\n\n    clutchless find ~/torrent_files -d ~/torrent_data\n\n\nTo organize torrents into folders under ``~/new_place`` and named by tracker, with ``default_folder`` for ones missing\na folder name for one reason or another::\n\n    clutchless organize ~/new_place -d default_folder\n\nRemove torrents that are completely missing data::\n\n    clutchless prune client\n\nRemove metainfo files from some folders (``folder1``, ``folder2``) that are found in Transmission::\n\n    clutchless prune folder ~/folder1 ~/folder2\n\nTo associate torrent to their matching data found in any number of folders (in this case just two)::\n\n    clutchless link ~/data_folder_1 ~/data_folder_2\n\nTo delete duplicate metainfo files in ``~/folder1``::\n\n    clutchless dedupe ~/folder1\n\nTo rename all the metainfo files in ``~/folder1`` according to metainfo (format: ``torrent_name.hash.torrent``)::\n\n    clutchless rename ~/folder1\n\n.. _developer documentation: DEVELOPER.rst",
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mhadam/clutchless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
