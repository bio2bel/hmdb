# -*- coding: utf-8 -*-

import logging
import os
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve
from zipfile import ZipFile

import time

from .constants import DATA_DIR, DATA_FILE_UNZIPPED, DATA_PATH, DATA_URL

log = logging.getLogger(__name__)


def download_data(force_download=False):
    """Downloads the data

    :param bool force_download: If true, overwrites a previously cached file
    :rtype: str
    """
    if os.path.exists(DATA_PATH) and not force_download:
        log.info('using cached data at %s', DATA_PATH)
    else:
        log.info('downloading %s to %s', DATA_URL, DATA_PATH)
        urlretrieve(DATA_URL, DATA_PATH)

    return DATA_PATH


def _ensure_data(force_download=False):
    if not os.path.exists(DATA_FILE_UNZIPPED):
        data_path = download_data(force_download=force_download)

        log.info('extracting %s to %s', data_path, DATA_FILE_UNZIPPED)
        with ZipFile(data_path) as f:
            f.extract(member='hmdb_metabolites.xml', path=DATA_DIR)

        assert os.path.exists(DATA_FILE_UNZIPPED)  # should correspond to this file

    return DATA_FILE_UNZIPPED


def get_data(source=None, force_download=False):
    """Parse .xml file into an ElementTree

    :param Optional[str] source: String representing the filename of a .xml file. If None the full HMDB metabolite .xml
                                 will be downloaded and parsed into a tree.
    :param bool force_download: Should the data be re-downloaded? Defaults to False.
    """
    if not source:
        source = _ensure_data(force_download=force_download)

    t = time.time()
    log.info('parsing %s', source)
    tree = ET.parse(source)
    log.info('done parsing after %.2f seconds', time.time() - t)

    return tree
