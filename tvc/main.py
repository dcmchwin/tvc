"""tvc main module: functions for command line interface to data
version control tool.

"""

import argparse
import logging
from tvc.init_dir import main as tvc_init
from tvc.add_extension import main as add_extension
from tvc.update_logs import main as update_logs
from tvc.pull import main as tvc_pull


# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def main():
    """Main function for parsing command line arguments."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='subparsers help',
                                       dest='subparser_name')

    # create parser for 'init' function
    parser_init = subparsers.add_parser('init',
                                        help='initiate a tvc repository')
    parser_init.add_argument('remote',
                             help='path to remote data repository',
                             default='hello')

    # create parser for 'pull' function
    parser_pull = subparsers.add_parser('pull',
                                        help='synch local data with remote')
    parser_pull.add_argument('--folder', default='C:\\Folder')

    # create parser for 'add_extension' function
    parser_add_extension = \
        subparsers.add_parser('add_extension',
                              help='add file extension to list of tracked file types')
    parser_add_extension.add_argument('extension', help='extension to track')

    # create parser for 'update_logs' function
    parser_update_logs = \
        subparsers.add_parser('update_logs',
                              help='update logs and hash associations of data')

    # parse command line arguments
    args = parser.parse_args()

    # switch to the right function for the input arguments
    subparser_funcs = dict(init=tvc_init,
                           pull=tvc_pull,
                           add_extension=add_extension,
                           update_logs=update_logs)
    subparser_funcs[args.subparser_name](args)


if __name__ == '__main__':
    main()
