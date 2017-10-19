"""Utilities common to all other modules in tvc."""
import csv
import json
import os
import time
from typing import Dict, List, Tuple

time_format = '%Y-%m-%dT%H:%M:%S%z'
local_log_fname = 'local_log.csv'
remote_log_fname = 'remote_log.csv'
config_fname = 'config'


def get_config_data(dot_tvc_dir: str) -> Dict[str, object]:
    """Get config data from config file in given .tvc directory.

    Parameters
    ----------
    dot_tvc_dir: str
        Path to .tvc directory

    Returns
    -------
    config_data: Dict[str: obj]
        configuration data for this tvc directory, including information
        like time of last update and path to remote data directory

    """
    # get required config data (path to remote dir, basically)
    config_path = os.path.join(dot_tvc_dir, config_fname)
    with open(config_path, 'r') as fin:
        config_data = json.load(fin)

    return config_data


def read_filepaths_and_md5_at_previous_update(
        dot_tvc_dir: str, log_filename: str) -> Tuple[List[str], List[str]]:
    """Read filepaths and hashes at previous update of remote log file.

    Parameters
    ----------
    dot_tvc_dir: str
        path to .tvc directory
    log_filename: str
        filename of the log file in the .tvc directory

    Returns
    -------
    filepath: List[str]
        List of filepaths in the log file
    md5: List[str]
        List of md5 hashes in the log file

    """
    # if no tvc directory specified, assume there is one in current directory
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    filename = []
    directory = []
    md5 = []

    # read contents of log file
    with open(os.path.join(dot_tvc_dir, log_filename)) as logf:
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


def modify_last_update_time() -> None:
    """Modify the 'last_update' time to now."""
    dot_tvc_dir = os.path.abspath('.tvc')
    config_path = os.path.join(dot_tvc_dir, 'config')
    data = get_config_data(dot_tvc_dir)

    data['last_update'] = time.strftime(time_format,
                                        time.gmtime())

    with open(config_path, 'w') as fout:
        json.dump(data, fout)