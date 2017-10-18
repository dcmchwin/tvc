"""Utilities common to all other modules in tvc."""
import json
import os
import time

time_format = '%Y-%m-%dT%H:%M:%S%z'
local_log_fname = 'local_hash_map.csv'
remote_log_fname = 'remote_log.csv'
config_fname = 'config'


def modify_last_update_time():
    """Modify the 'last_update' time to now."""
    config_path = os.path.join('.tvc', 'config')

    with open(config_path, 'r') as fin:
        data = json.load(fin)

    data['last_update'] = time.strftime(time_format,
                                        time.gmtime())

    with open(config_path, 'w') as fout:
        json.dump(data, fout)