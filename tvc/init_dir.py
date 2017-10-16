"""Functions to support initialisation of .tvc directory."""
import hashlib
import json
import logging
import os

# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def main(args):
    _mk_tvc_dir(args)
    _mk_config(args)


def _mk_tvc_dir(args):
    """Make .tvc directory at current location."""
    if not os.path.isdir(args.remote):
        raise FileExistsError('{} not an accessible directory location'.
                              format(args.remote))

    try:
        os.mkdir('.tvc')
    except FileExistsError:
        logger.info('.tvc folder already exists in this directory')
        return


def _mk_config(args):
    """Make config file in .tvc directory."""
    data = dict(remote=args.remote,
                tracked_extensions=[])
    f = open(os.path.join('.tvc', 'config'), 'w')
    json.dump(data, f)
    f.close()


def _mk_logs():
    """Make empty log files for remote contents and local mappings."""
    open(os.path.join('.tvc', 'remote_log.csv')).close()
    open(os.path.join('.tvc', 'local_hash_map.csv')).close()
