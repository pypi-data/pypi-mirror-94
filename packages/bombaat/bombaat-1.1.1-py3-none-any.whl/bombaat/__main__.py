#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main Module"""

import sys
import logging

from bombaat import __version__
from bombaat.errors import bombaatCloudError
from bombaat.argparser import create_argument_parser

logger = logging.getLogger(__name__)

def print_version() -> None:
    sys.stdout.write(f'\nbombaat version {__version__}' + '\n')


def main() -> None:
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    try:
        if hasattr(cmdline_arguments, 'func'):
            cmdline_arguments.func(cmdline_arguments)
        elif hasattr(cmdline_arguments, 'version'):
            print_version()
        else:
            # user has not provided a subcommand, let's print the help
            arg_parser.print_help()
            sys.exit(1)
    except bombaatCloudError as err:
        logger.info('\nFailed to run bombaat CLI due to an exception: %s'% (
                                                                    str(err),))
        sys.exit(1)


if __name__=='__main__':
    main()
