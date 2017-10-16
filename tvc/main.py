import argparse
import json
import logging
import os


# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def tvc_init(args):
    """Make .tvc directory at current location."""

    if not os.path.isdir(args.remote):
        raise FileExistsError('{} not an accessible directory location'.
                              format(args.remote))

    try:
        os.mkdir('.tvc')
    except FileExistsError as e:
        logger.info('.tvc folder already exists in this directory')
        return

    data = dict(remote=args.remote)
    f = open(os.path.join('.tvc', 'config'), 'w')
    json.dump(data, f)
    f.close()


def tvc_pull(args):
    logger.debug('Not Implemented')


def main():
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

    # parse command line arguments
    args = parser.parse_args()

    # switch to the right function for the input arguments
    subparser_funcs = dict(init=tvc_init,
                           pull=tvc_pull)
    subparser_funcs[args.subparser_name](args)


if __name__ == '__main__':
    main()
