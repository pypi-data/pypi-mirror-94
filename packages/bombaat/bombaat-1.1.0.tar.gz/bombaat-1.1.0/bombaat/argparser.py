#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Argument Parser Module"""

import sys
import logging
import argparse

from typing import List, Text

from bombaat.login import Login
from bombaat.utils import print_msg
from bombaat.configure import Configure
from bombaat.driver import update_driver
from bombaat.profiles import download_profile
from bombaat.init import update_downloader_path

logger = logging.getLogger(__name__)

SubParsersAction = argparse._SubParsersAction

HELP_BLURB = (
    '\nTo see help text, you can run:\n'
    '\n'
    '  bombaat --help\n'
    '  bombaat <command> --help' + '\n'
)

def create_argument_parser() -> argparse.ArgumentParser:
    """Parse all the command line arguments."""

    parser = argparse.ArgumentParser(
        prog='bombaat',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='bombaat command line interface. bombaat CLI enables '
                    'you to access AWS Cloud Accounts using Azure single '
                    'sign on service via `awscli` or `boto`.',)

    parser.add_argument(
        '--version',
        action='store_true',
        default=argparse.SUPPRESS,
        help='print installed bombaat CLI version',)

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parsers = [parent_parser]
    subparsers = parser.add_subparsers(help='bombaat CLI commands')

    init_subparser(subparsers, parents=parent_parsers)
    update_subparser(subparsers, parents=parent_parsers)
    configure_subparser(subparsers, parents=parent_parsers)
    login_subparser(subparsers, parents=parent_parsers)
    return parser

def init_subparser(subparsers: SubParsersAction,
                    parents: List[argparse.ArgumentParser]) -> None:
    """Init parsers."""

    login_parser = subparsers.add_parser(
        'init',
        parents=parents,
        help='Initialize downloader host.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
    login_parser.set_defaults(func=run_init)


def run_init(args: argparse.Namespace) -> None:
    update_downloader_path()


def update_subparser(subparsers: SubParsersAction,
                        parents: List[argparse.ArgumentParser]) -> None:
    """update parsers."""

    configure_parser = subparsers.add_parser(
        'update',
        conflict_handler='resolve',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=parents,
        help='Install a new profile and drivers.',)

    configure_parser.add_argument('configure_option',
                                help= 'update bombaat config.',
                                choices=['all', 'profile', 'config',])

    configure_parser.set_defaults(func=run_update)


def run_update(args: argparse.Namespace) -> None:
    msg = f'Please wait while setup installs necessary configuration files.'
    print_msg(msg)
    sys.stdout.write('\n')
    if args.configure_option == 'all':
        update_driver()
        sys.stdout.write('\n')
        download_profile()
        print_msg('Update completed.\n')
        print_msg(HELP_BLURB)
    elif args.configure_option == 'profile':
        download_profile()
        print_msg('Profiles update completed.\n')
    elif args.configure_option == 'config':
        update_driver()
        print_msg('Config update completed.\n')


def configure_subparser(subparsers: SubParsersAction,
                    parents: List[argparse.ArgumentParser]) -> None:
    """Login parsers."""

    login_parser = subparsers.add_parser(
        'configure',
        parents=parents,
        help='Configure cloud profile.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
    login_parser.set_defaults(func=run_configure)


def run_configure(args: argparse.Namespace) -> None:
    Configure().main()


def login_subparser(subparsers: SubParsersAction,
                    parents: List[argparse.ArgumentParser]) -> None:
    """Login parsers."""

    login_parser = subparsers.add_parser(
        'login',
        parents=parents,
        help='Log in to a cloud profile.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
    login_parser.set_defaults(func=run_login)


def run_login(args: argparse.Namespace) -> None:
    Login().main()
