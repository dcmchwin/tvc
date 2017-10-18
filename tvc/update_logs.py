"""Module to update logs to agree with list of tracked extensions."""
import csv
import hashlib
import json
import logging
import os
from datetime import datetime
from tvc.utils import local_log_fname, remote_log_fname, config_fname,\
    time_format, modify_last_update_time, read_filepaths_and_md5_at_previous_update


# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def main(args):
    """Update the logs."""
    # assume that local data dir is current dir
    local_data_dir = os.path.abspath('')
    dot_tvc_dir = os.path.join(local_data_dir, '.tvc')

    # get required config data (path to remote dir, basically)
    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        config_data = json.load(fin)

    # make remote log
    logger.info('\nUPDATING LOG OF REMOTE DATA')
    mk_log(dot_tvc_dir, config_data['remote'], remote_log_fname)

    # make local log
    logger.info('\nUPDATING LOG OF LOCAL DATA')
    mk_log(dot_tvc_dir, local_data_dir, local_log_fname)

    # modify the last update time
    modify_last_update_time()


def mk_log(dot_tvc_dir, data_dir, log_filename):
    """Get csv mapping hash files."""
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        config_data = json.load(fin)

    # Get list of filenames and folders
    filename, directory, filepath = \
        _read_all_possible_tracked_files(data_dir,
                                         config_data['tracked_extensions'])

    # Init empty md5 list
    md5 = [None] * len(filename)

    # Get list of filepaths and hashes at last update
    filepath_lu, md5_lu = \
        read_filepaths_and_md5_at_previous_update(dot_tvc_dir, log_filename)

    for i, fp in enumerate(filepath):
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


def _read_all_possible_tracked_files(data_dir,
                                     tracked_extensions):
    """Get lists of filepaths, names and folders for tracked files."""
    directory = []  # directory path is relative to remote_folder_path
    filename = []
    filepath = []

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


def is_recently_altered(filepath, last_update_string):
    """Determine whether a file is newly created or recently modified."""
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
    """Get md5 hash of contents of file at given absolute path."""
    blocksize = 2 ** 12
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


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
