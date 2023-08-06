#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SSO driver files updater."""

import os
import sys
import stat
import shutil
import logging
from pathlib import Path

from bombaat.downloader import get_url
from bombaat.downloader import extract_zip
from bombaat.downloader import download_zip
from bombaat.init import get_download_host_url
from bombaat.downloader import current_platform
from bombaat.downloader import config_executable
from bombaat.downloader import clear_cache_folders

from bombaat import __bombaat_home__

logger = logging.getLogger(__name__)

DOWNLOADS_FOLDER = Path(__bombaat_home__)
BASE_URL = os.environ.get('BOMBAAT_DOWNLOAD_HOST', get_download_host_url())


DRIVER_FOLDER = 'driver'

drivers_file = {'mac':'mac-drivers.zip', 'linux': 'linux-drivers.zip'}

chrome_folder = {'mac': 'chrome-mac', 'linux': 'chrome-linux' }

download_urls = {'mac': f'{BASE_URL}/{drivers_file[current_platform()]}',
                 'linux': f'{BASE_URL}/{drivers_file[current_platform()]}'}

config_files = {'mac': [(DOWNLOADS_FOLDER / 'driver' / 'chromedriver'),
                        (DOWNLOADS_FOLDER / 'chrome-mac' / 'Chromium.app' /
                                        'Contents' / 'MacOS' / 'Chromium')],
                'linux': [(DOWNLOADS_FOLDER / 'driver' / 'chromedriver'),
                        (DOWNLOADS_FOLDER / chrome_folder[current_platform()] /
                                                                   'chrome')]}


def download_driver() -> None:
    """Download and extract driver files."""
    DRIVERS_FILE = drivers_file[current_platform()]
    extract_zip(download_zip(get_url(download_urls)),
                                    DOWNLOADS_FOLDER,
                                    drivers_file[current_platform()])
    zip_path = DOWNLOADS_FOLDER / drivers_file[current_platform()]

    if check_driver() and zip_path.exists():
        zip_path.unlink()

    if not check_driver():
        raise IOError('Failed to extract drivers.')

    for exec_path in config_executable(config_files):
        if 'chrome' in str(exec_path).lower():
            exec_path.chmod(exec_path.stat().st_mode | stat.S_IXOTH |
                                            stat.S_IXGRP | stat.S_IXUSR)


def check_driver() -> bool:
    """Check if driver files are placed at correct path."""
    return config_executable(config_files)[0].exists() and \
           config_executable(config_files)[1].exists()


def get_driver_file() -> str:
    """Get profile file."""
    if check_driver():
        return config_executable(config_files)
    logger.error(('Required config files are missing, you can run'
                ' `bombaat update config` to update config files.'))
    sys.exit(1)


def update_driver() -> None:
    """update drivers"""
    chrome_folder_path = DOWNLOADS_FOLDER / chrome_folder[current_platform()]
    if chrome_folder_path.exists():
        shutil.rmtree(chrome_folder_path)

    driver_folder_path = DOWNLOADS_FOLDER / DRIVER_FOLDER
    if driver_folder_path.exists():
        shutil.rmtree(driver_folder_path)

    clear_cache_folders()
    download_driver()
