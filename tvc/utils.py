"""Utilities common to all other modules in tvc."""
import csv
import json
import os
import time

time_format = '%Y-%m-%dT%H:%M:%S%z'
local_log_fname = 'local_hash_map.csv'
remote_log_fname = 'remote_log.csv'
config_fname = 'config'


def read_filepaths_and_md5_at_previous_update(dot_tvc_dir, log_filename):
    """Read filepaths at previous update of remote log file."""
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')
    filename = []
    directory = []
    md5 = []
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


def modify_last_update_time():
    """Modify the 'last_update' time to now."""
    config_path = os.path.join('.tvc', 'config')

    with open(config_path, 'r') as fin:
        data = json.load(fin)

    data['last_update'] = time.strftime(time_format,
                                        time.gmtime())

    with open(config_path, 'w') as fout:
        json.dump(data, fout)