#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SSO config files updater module."""

import os
import sys
import shutil
import logging
import subprocess
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import urllib3
from tqdm import tqdm

from bombaat import __bombaat_home__

logger = logging.getLogger(__name__)

DOWNLOADS_FOLDER = Path(__bombaat_home__)

NO_PROGRESS_BAR = os.environ.get('BOMBAAT_NO_PROGRESS_BAR', '')

if NO_PROGRESS_BAR.lower() in ('1', 'true'):
    NO_PROGRESS_BAR = True  # type: ignore


def current_platform() -> str:
    """Get current platform name by short string."""

    if sys.platform.startswith('darwin'):
        return 'mac'
    if sys.platform.startswith('linux'):
        return 'linux'
    raise OSError('Unsupported platform: ' + sys.platform)


def get_url(download_urls: dict) -> str:
    """Get download url."""
    return download_urls[current_platform()]


def download_zip(url: str) -> BytesIO:
    """Download data from url."""

    # disable warnings so that we don't need a cert.
    # see https://urllib3.readthedocs.io/en/latest/advanced-usage.html for more
    urllib3.disable_warnings()

    with urllib3.PoolManager() as http:
        # Get data from url.
        # set preload_content=False means using stream later.
        data = http.request('GET', url, preload_content=False)

        try:
            total_length = int(data.headers['content-length'])
        except (KeyError, ValueError, AttributeError):
            total_length = 0

        process_bar = tqdm(total=total_length,
                                file=os.devnull if NO_PROGRESS_BAR else None,)

        # 10 * 1024
        _data = BytesIO()
        for chunk in data.stream(10240):
            _data.write(chunk)
            process_bar.update(len(chunk))
        process_bar.close()

    return _data


def extract_zip(data: BytesIO, path: Path, download_file: str) -> None:
    """Extract zipped data to path."""

    msg = (f'Failed to update SSO configuration, something went wrong.')

    # On mac zipfile module cannot extract correctly, so use unzip instead.
    if current_platform() == 'mac':
        zip_path = path / download_file
        if not path.exists():
            path.mkdir(parents=True)
        with zip_path.open('wb') as f:
            f.write(data.getvalue())
        if not shutil.which('unzip'):
            logger.error(msg)
            sys.exit(1)

        proc = subprocess.run(['unzip', str(zip_path)],
                                cwd=str(path),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,)

        if proc.returncode != 0:
            sys.stdout.write(proc.stdout.decode())
            logger.error(msg)
            sys.exit(1)
    else:
        with ZipFile(data) as zf:
            zf.extractall(str(path))


def config_executable(config_files: dict) -> Path:
    """Get path of the executable."""
    return config_files[current_platform()]


def clear_cache_folders() -> None:
    """Clear cache store to avoid zip extraction."""
    CACHE_FOLDER = '__MACOSX'
    cache_folder_path = DOWNLOADS_FOLDER / CACHE_FOLDER
    if cache_folder_path.exists():
        shutil.rmtree(cache_folder_path)
