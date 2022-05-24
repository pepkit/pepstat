import sys
from logging import getLogger

import logmuse
from ubiquerg import expandpath

from .argparser import build_argparser
from .const import *
from .exceptions import *

_LOGGER = getLogger(PKG_NAME)


def main():
    """Primary workflow"""
    from inspect import getdoc

    parser = logmuse.add_logging_options(build_argparser("PEPHub repository indexer."))
    args = parser.parse_args()
    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args, make_root=True)
    _LOGGER.debug("Args namespace:\n{}".format(args))

    if args.command == INDEX_CMD:
        _LOGGER.info("Running")
    else:
        raise UnknwownCommandError(f"Received unknown command: {args.command}")

    sys.exit(0)
