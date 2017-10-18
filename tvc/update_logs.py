"""Module to update logs to agree with list of tracked extensions."""
import csv
import hashlib
import json
import logging
import os
from time import strptime, mktime
from tvc.utils import remote_log_fname, config_fname, time_format


# Set logger up for module
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def main(args):
    mk_remote_log()


def mk_local_hash_map():
    pass


def mk_remote_log(dot_tvc_dir=None):
    """Get csv mapping hash files."""
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        data = json.load(fin)

    # Get list of filenames and folders
    filename, directory, filepath =\
        _read_all_possible_tracked_files(data['remote'],
                                         data['tracked_extensions'])

    # Init empty md5 list
    md5 = [None] * len(filename)

    # Get list of filepaths and hashes at last update
    filepath_lu, md5_lu = \
        _read_filepaths_and_md5_at_previous_update(dot_tvc_dir)

    for i, fp in enumerate(filepath):
        fp_full = os.path.join(data['remote'], fp)

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
        last_update_time = mktime(strptime(data['last_update'],
                                           time_format))
        has_changed = is_recently_altered(fp_full, last_update_time)
        if has_changed or not fp_in_last_update:
            logger.info('File {} of {}\nHashing {}'.
                        format(i + 1, len(filepath), fp))
            md5[i] = get_md5_hash(fp_full)
        else:
            logger.debug('File {} of {}\nSkipping Hash {}'.
                        format(i + 1, len(filepath), fp))
            md5[i] = md5_lu[j]

    # Rewrite log file contents
    with open(os.path.join(dot_tvc_dir, remote_log_fname),
              'w', newline='') as logf:
        csv_writer = csv.writer(logf)
        csv_writer.writerow(['md5', 'filename', 'directory'])
        for i, fn in enumerate(filename):
            csv_writer.writerow([md5[i], fn, directory[i]])


def _read_all_possible_tracked_files(remote_folder_path,
                                     tracked_extensions):
    """Get lists of filepaths, names and folders for tracked files."""
    directory = []
    filename = []
    filepath = []

    def getext(s): return os.path.splitext(s)[1]

    for root, _, names in os.walk(remote_folder_path, topdown=True):
        names = [n for n in names
                 if getext(n) in tracked_extensions]
        filename.extend(names)
        directory.extend([root] * len(names))
        filepath.extend([os.path.join(root, fn) for fn in names])

    return filename, directory, filepath


def _read_filepaths_and_md5_at_previous_update(dot_tvc_dir=None):
    """Read filepaths at previous update of remote log file."""
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')
    filename = []
    directory = []
    md5 = []
    with open(os.path.join(dot_tvc_dir, remote_log_fname)) as logf:
        csv_reader = csv.reader(logf)
        next(csv_reader)  # skip header row
        # below relies on column format being: (md5 hash, filename, folder)
        for row in csv_reader:
            # skip empty rows
            if row:
                md5.append(row[0])
                filename.append(row[1])
                directory.append(row[2])
    filepath = [os.path.join(d, f)
                for d, f in zip(directory, filename)]

    return filepath, md5


def is_recently_altered(filepath, last_update_time):
    """Determine whether a file is newly created or recently modified."""
    stats = os.stat(filepath)
    modify_time = stats.st_mtime
    creation_time = stats.st_ctime
    if last_update_time < modify_time or last_update_time < creation_time:
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

    mk_remote_log(dot_tvc_dir)