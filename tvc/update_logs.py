"""Module to update logs to agree with list of tracked extensions."""

from argparse import Namespace
import csv
import hashlib
import json
import logging
import os
from datetime import datetime
from tvc.utils import local_log_fname, remote_log_fname, config_fname,\
    time_format, modify_last_update_time, read_filepaths_and_md5_at_previous_update,\
    get_config_data
from typing import List, Tuple

# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def main(args: Namespace, dot_tvc_dir: str=None) -> None:
    """Update the remote and local logs.

    This function updates the local log file so that it lists filepaths
    and md5 hashes of all the tracked files in the local data directory.
    It then performs the same function for the files in the remote
    data directory. Finally, 'time of last update' field in the config
    file is updated.

    Parameters
    ----------
    args: Namespace
        Command line arguments passed to the update_logs function
    dot_tvc_dir: str
        path to .tvc directory
    """
    if dot_tvc_dir is None:
        # assume that local data dir is current dir
        dot_tvc_dir = os.path.abspath('.tvc')

    local_data_dir = os.path.dirname(dot_tvc_dir)

    config_data = get_config_data(dot_tvc_dir)

    # make remote log
    logger.info('\nUPDATING LOG OF REMOTE DATA')
    mk_log(dot_tvc_dir, config_data['remote'], remote_log_fname)

    # make local log
    logger.info('\nUPDATING LOG OF LOCAL DATA')
    mk_log(dot_tvc_dir, local_data_dir, local_log_fname)

    # modify the last update time
    modify_last_update_time(dot_tvc_dir)


def mk_log(dot_tvc_dir: str, data_dir: str, log_filename: str) -> None:
    """Get csv mapping hash files.

    Update a specified log file in the specified .tvc directory to list
    the tracked contents of the specified data directory. File md5 hashes
    are only recalculated if:
        - The file is of a tracked type
        AND AT LEAST ONE OF
        - The file has been modified since the last update time (in config)
        - The file has been created in this directory since the last update time
        - The file was not tracked at the last update
    A log file is saved at the end of this function.

    Parameters
    ----------
    dot_tvc_dir: str
        filepath to the .tvc directory
    data_dir: str
        absolute filepath to the data directory (local or remote)
    log_filename: str
        name of the log file (in the .tvc directory) to update

    Returns
    -------

    """
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    config_data = get_config_data(dot_tvc_dir)

    # Get list of filenames and folders
    filename, directory, filepath = \
        _read_all_possible_tracked_files(data_dir,
                                         config_data['tracked_extensions'])

    # Instantiate empty md5 list
    md5 = [None] * len(filename)

    # Get list of filepaths and hashes at last update
    filepath_lu, md5_lu = \
        read_filepaths_and_md5_at_previous_update(dot_tvc_dir, log_filename)

    for i, fp in enumerate(filepath):

        # get absolute paths of all the data files
        fp_full = os.path.join(data_dir, fp)

        # get index of where filepath exists in list of
        # old filepaths
        if fp in filepath_lu:
            j = filepath_lu.index(fp)
            fp_in_last_update = True
        else:
            fp_in_last_update = False

        # calculate md5 hash if filename is not already present
        # in the list of filenames made at last update OR if it
        # has been altered since the last update
        has_changed = is_recently_altered(fp_full, config_data['last_update'])
        if has_changed or not fp_in_last_update:
            logger.info('File {} of {}\nHashing {}'.
                        format(i + 1, len(filepath), fp))
            md5[i] = get_md5_hash(fp_full)
        else:
            logger.debug('File {} of {}\nSkipping Hash {}'.
                         format(i + 1, len(filepath), fp))
            md5[i] = md5_lu[j]

    # Rewrite log file contents
    with open(os.path.join(dot_tvc_dir, log_filename),
              'w', newline='') as logf:
        csv_writer = csv.writer(logf)
        csv_writer.writerow(['md5', 'filename', 'directory'])
        for i, fn in enumerate(filename):
            csv_writer.writerow([md5[i], fn, directory[i]])


def _read_all_possible_tracked_files(\
        data_dir: str, tracked_extensions: List[str]) -> \
        Tuple[List[str], List[str], List[str]]:
    """Get lists of filepaths, names and folders for tracked files.

    Walk through a given data directory, and find all files of matching
    the given list of matched extension types. Return a list of the names
    of these files, a list of the relative paths to these files from
    the data directory, and a list of the relative paths to the directories
    of these files from the data directory.

    Parameters
    ----------
    data_dir: str
        Absolute filepath of data directory to walk through
    tracked_extensions: List[str]
        List of tracked extensions

    Returns
    -------
    filename: List[str]
        List of filenames of files to track
    directory: List[str]
        List of relative paths (from data_dir) of files to tracks
    filepath: List[str]
        List of relative paths (from data_dir) of files to tracks

    """
    directory = []  # directory path is relative to data_dir
    filename = []
    filepath = []

    # helper function to get file extension
    def getext(s): return os.path.splitext(s)[1]

    # ensure directory path is relative to remote folder path
    start_idx = len(data_dir) + len(os.sep)
    def shorten(s): return s[start_idx:]

    for root, _, names in os.walk(data_dir, topdown=True):
        names = [n for n in names
                 if getext(n) in tracked_extensions]
        filename.extend(names)
        directory.extend([shorten(root)] * len(names))
        filepath.extend([os.path.join(shorten(root), fn) for fn in names])

    return filename, directory, filepath


def is_recently_altered(filepath: str, last_update_string: str) -> bool:
    """Determine whether a file is newly created, or recently modified.

    Folder system is used to interrogate 'creation time' and 'modification
    time' of the file in question.

    Parameters
    ----------
    filepath: str
        Path to file to investigate
    last_update_string: str
        string indicating last update time (from .tvc/config), formatted
        according to time_format

    Returns
    -------
    output: bool
        logical for whether file has been recently altered or not

    """
    # Get time in seconds of last update time, assuming time was recorded
    # as per time_format
    last_update_datetime = datetime.strptime(last_update_string,
                                             time_format)
    last_update_timestamp = last_update_datetime.timestamp()

    # Get timestamps for file modification and creation times
    # (Creation time tells you when the file was added to its current folder
    # and modification time tells you when the file was last modified)
    stats = os.stat(filepath)
    modify_time = stats.st_mtime
    creation_time = stats.st_ctime

    if (last_update_timestamp < modify_time
        or last_update_timestamp < creation_time):
        output = True
    else:
        output = False
    return output



def get_md5_hash(filepath):
    """Get md5 hash of entire data file at specified filepath.

    Parameters
    ----------
    filepath: str
        path to the input data file

    Returns
    -------
    md5_hash: str
        md5 hash of input file

    """
    # Read in chunks of file sequentially, in units of size blocksize
    blocksize = 2 ** 12
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hasher.update(chunk)
    md5_hash = hasher.hexdigest()
    return md5_hash


if __name__ == "__main__":
    # folder = "P:\P29xx\P2976_Calcutta\Misc\\videos\mackle_apple_orchard"
    # tracked_extensions = ['.mp4']
    # fn, d, fp = _read_all_possible_tracked_files(folder, tracked_extensions)
    # print(fn, d, fp)

    dot_tvc_dir = 'C:\\Users\\dcm\\Documents\\Git\\tvc\\data\\.tvc'
    # filepath, md5 = _read_filepaths_and_md5_at_previous_update(dot_tvc_dir)
    # print(filepath)

    # # get required config data (path to remote dir, basically)
    # dot_tvc_dir = 'C:\\Users\\dcm\\Documents\\Git\\tvc\\data\\.tvc'
    # config_path = os.path.join(dot_tvc_dir, config_fname)
    # with open(config_path, 'r') as fin:
    #     config_data = json.load(fin)
    #
    # mk_log(dot_tvc_dir, config_data['remote'], remote_log_fname)

    # get required config data (path to remote dir, basically)
    local_data_dir = 'C:\\Users\\dcm\\Documents\\Git\\tvc\\data'
    dot_tvc_dir = os.path.join(local_data_dir, '.tvc')
    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        config_data = json.load(fin)

    mk_log(dot_tvc_dir, local_data_dir, local_log_fname)
