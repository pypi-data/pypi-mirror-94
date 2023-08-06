#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SSO profile files udpater."""

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

PROFILE_FILE = 'profiles.zip'
PROFILE_FOLDER = 'profiles'

download_urls = f'{BASE_URL}/{PROFILE_FILE}'

config_files = (DOWNLOADS_FOLDER / PROFILE_FOLDER / 'sso.yml')


def download_profile() -> None:
    """Download and extract profile file."""

    profile_folder_path = DOWNLOADS_FOLDER / PROFILE_FOLDER
    if profile_folder_path.exists():
        shutil.rmtree(profile_folder_path)

    clear_cache_folders()

    extract_zip(download_zip(download_urls), DOWNLOADS_FOLDER, PROFILE_FILE)

    zip_path = DOWNLOADS_FOLDER / PROFILE_FILE

    if zip_path.exists():
        zip_path.unlink()

    if not check_profile():
        logger.error('Failed to update cloud profiles.')


def check_profile() -> bool:
    """Check if profile files are placed at correct path."""
    return config_files.exists()


def get_profile_file() -> str:
    """Get profile file."""
    if check_profile():
        return config_files
    logger.error('\nLooks like SSO profile file is missing, '
                    'you can run `bombaat update profile` to udpate profiles.')
    sys.exit(1)
