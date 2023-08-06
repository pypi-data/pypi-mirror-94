#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Common utilities."""

import os
import sys
import logging
from dateutil import tz
from collections import namedtuple

import yaml
import inquirer

from blessed import Terminal
from inquirer.themes import Theme

from bombaat.errors import SSOFileReadError
from bombaat.errors import FileNotFoundError
from bombaat.profiles import get_profile_file

logger = logging.getLogger(__name__)

term = Terminal()

class MorningSun(Theme):

    term = Terminal()

    def __init__(self) -> None:
        super(MorningSun, self).__init__()
        self.Question.mark_color = self.term.bright_white
        self.Question.brackets_color = self.term.bright_white
        self.Question.default_color = self.term.bright_white
        self.Editor.opening_prompt_color = self.term.bright_black
        self.Checkbox.selection_color = self.term.red
        self.Checkbox.selection_icon = '>'
        self.Checkbox.selected_icon = 'X'
        self.Checkbox.selected_color = self.term.yellow + self.term.bold
        self.Checkbox.unselected_color = self.term.normal
        self.Checkbox.unselected_icon = 'o'
        self.List.selection_color = self.term.black_on_lightskyblue4
        self.List.selection_cursor = '>'
        self.List.unselected_color = self.term.lightskyblue3


def read_yaml(file_name: str) -> dict:
    """Read configuration from YAML file."""

    if not os.path.exists(file_name):
        logger.error(f'Cloud config file {file_name} does not exist!')
        raise FileNotFoundError()
    try:
        with open(file_name, 'r') as fh:
            return yaml.safe_load(fh)
    except Exception as err:
        raise SSOFileReadError(
                        'Unable to read SSO config: %s' % (str(err),))
        sys.exit(1)

def write_yaml(file_name: str, data: dict) -> None:
    """YAML Writer."""
    with open(file_name, 'w') as fh:
        yaml.dump(data, fh)

def get_cloud_profiles() -> dict:
    """Get cloud profiles from yaml."""
    return read_yaml(str(get_profile_file()))


def ask(msg: str, choice_list: list) -> str:
    sys.stdout.write(term.homes + term.clear)
    _questions = [inquirer.List('choice',
                        message=term.bright_white +
                        msg +
                        term.deepskyblue,
                        choices=choice_list,),]
    _answers = inquirer.prompt(_questions,theme=MorningSun())
    return _answers


def datetime_utc_to_local(utc_time: str) -> str:
    """Convert UTC time to Local time"""
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = utc_time.replace(tzinfo=from_zone)
    local_time = utc.astimezone(to_zone)
    local_time = local_time.strftime('%Y-%m-%d %I:%M %p')
    return local_time


def print_msg(msg):
    return sys.stdout.write(term.white(f'{msg}'))
