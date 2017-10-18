"""Functions to support initialisation of .tvc directory."""
import csv
import hashlib
import json
import logging
import os
from tvc.utils import local_hashmap_fname, modify_last_update_time,\
        remote_log_fname, config_fname

# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def main(args):
    _mk_tvc_dir(args)
    _mk_config(args)
    _mk_logs()
    modify_last_update_time()


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
    f = open(os.path.join('.tvc', config_fname), 'w')
    json.dump(data, f)
    f.close()


def _mk_logs(dot_tvc_dir=None):
    """Make empty log files for remote contents and local mappings."""
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    with open(os.path.join(dot_tvc_dir, remote_log_fname),
              'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['md5', 'filename', 'directory'])
    with open(os.path.join(dot_tvc_dir, local_hashmap_fname),
              'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['md5', 'filename'])
