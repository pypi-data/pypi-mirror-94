
import os
import sys
import logging
from pathlib import Path

import yaml

from bombaat import __bombaat_home__, __default_download_host__

logger = logging.getLogger(__name__)

DOWNLOADS_FOLDER = Path(__bombaat_home__)

download_host_file = DOWNLOADS_FOLDER / 'downloader.yaml'

def update_downloader_path() -> None:
    """Update download url."""

    if download_host_file.exists():
        os.remove(download_host_file)

    host = input('Please enter the download host url '
                                '(ex: http://example.com): ')

    with open(download_host_file, 'w') as fh:
        yaml.dump({'host': host}, fh)

def get_download_host_url() -> str:
    """Host handler."""

    if download_host_file.exists():
        with open(download_host_file) as fh:
            host = yaml.full_load(fh)
            if host is not None and 'host' in host:
                return host['host']
    return __default_download_host__
