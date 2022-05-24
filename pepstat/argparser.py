import argparse

from ubiquerg import VersionInHelpParser

from ._version import __version__
from .const import *

def build_argparser(desc):
    """
    Builds argument parser.
    :param str desc: additional description to print in help
    :return argparse.ArgumentParser
    """
    banner = "%(prog)s - report pipeline results"
    additional_description = desc
    parser = VersionInHelpParser(
        version=__version__, description=banner, epilog=additional_description
    )

    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {v}".format(v=__version__)
    )

    subparsers = parser.add_subparsers(dest="command")

    def add_subparser(cmd, msg):
        return subparsers.add_parser(
            cmd,
            description=msg,
            help=msg,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=40, width=90
            ),
        )

    sps = {}
    sps[INDEX_CMD] = add_subparser(INDEX_CMD, "Index a repository of peps.")
    sps[INDEX_CMD].add_argument(
        "-p",
        "--path",
        dest="path",
        required=True,
        help="Path/URL to PEP repository."
    )

    return parser
