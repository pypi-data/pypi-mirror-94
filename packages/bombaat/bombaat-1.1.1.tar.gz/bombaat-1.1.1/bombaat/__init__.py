#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Metadata for bombaat."""

import os
import sys
import logging

from appdirs import AppDirs
from colorlog import ColoredFormatter

__author__ = """Ravi Boodher"""
__email__ = 'boodher@gmail.com'
__version__ = '1.0.1'
__status__ = "Production"
__bombaat_home__ = os.environ.get(
    'BOMBAAT_HOME', AppDirs('bombaat').user_data_dir)  # type: str
__default_download_host__ = 'https://bombaat.s3.ap-south-1.amazonaws.com'
DEBUG = False

# Create a root logger
logger = logging.getLogger('bombaat')
log_level = logging.INFO
log_format = '%(log_color)s%(message)s%(reset)s'
formatter = ColoredFormatter(log_format)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)
stream_handler.setFormatter(formatter)
logger.setLevel(log_level)
logger.addHandler(stream_handler)

def exception_handler(exception_type, exception, traceback):
    # All your trace are belong to us!
    # your format
    print(exception_type.__name__, exception)

sys.excepthook = exception_handler
