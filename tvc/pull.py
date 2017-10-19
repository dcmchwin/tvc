"""Module for pulling down data from remote to local."""

import shutil
import json
import logging
import os
from tvc.utils import local_log_fname, remote_log_fname, config_fname,\
    time_format, modify_last_update_time, read_filepaths_and_md5_at_previous_update


# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def main(args):
    """Copy tracked files from remote to local.

    Parameters
    ----------
    args: Namespace
        Command line arguments passed to the pull function
    """
    # assume that local data dir is current dir
    local_data_dir = os.path.abspath('')
    dot_tvc_dir = os.path.join(local_data_dir, '.tvc')

    # get required config data (path to remote dir, basically)
    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        config_data = json.load(fin)

    # Get local filepaths (relative to local data dir) and md5 hashes
    filepath_relative_local, md5_local =\
        read_filepaths_and_md5_at_previous_update(dot_tvc_dir, local_log_fname)

    # Get remote filepaths (relative to remote data dir) and md5 hashes
    filepath_relative_remote, md5_remote = \
        read_filepaths_and_md5_at_previous_update(dot_tvc_dir, remote_log_fname)

    # Get full filepaths for remote and local data
    filepath_remote = [os.path.join(config_data['remote'], fp)
                       for fp in filepath_relative_remote]
    filepath_local = [os.path.join(local_data_dir, fp)
                      for fp in filepath_relative_local]

    # Create list of source and destination files to copy over,
    # using presence of local hash in remote hash list as copy criterion
    remote_files_to_copy = []
    local_files_to_copy = []
    for i, md5 in enumerate(md5_local):
        try:
            j = md5_remote.index(md5)
        except ValueError:
            logger.warning('{} with md5 hash {} has no corresponding hash in {}'.
                           format(filepath_relative_local[i],
                                  md5,
                                  remote_log_fname)
                           )
            continue
        remote_files_to_copy.append(filepath_remote[j])
        local_files_to_copy.append(filepath_local[i])

    # Copy over files from remote to local
    for src, dst in zip(remote_files_to_copy, local_files_to_copy):
        logger.info('Copying {} to {}'.format(src, dst))
        shutil.copy2(src, dst)

    modify_last_update_time()
