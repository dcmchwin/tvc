"""Test functions in tvc.utils."""

from argparse import Namespace
import csv
from datetime import datetime
import json
import time
import os
import pytest
from tvc.utils import modify_last_update_time,\
    read_filepaths_and_md5_at_previous_update,\
    time_format, config_fname


def test_read_filepaths_and_md5_at_previous_update(tmpdir):
    """Test that log files are properly read."""
    # make a fake log file with one entry
    dot_tvc_dir = str(tmpdir)
    log_fname = 'log.csv'
    log_fp = os.path.join(dot_tvc_dir, log_fname)
    with open(log_fp, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['md5', 'filename', 'directory'])
        data_row = ['a', 'b', 'c']
        csv_writer.writerow(data_row)

    # now read in the contents of the same log file and verify its contents
    fp, md5 = read_filepaths_and_md5_at_previous_update(dot_tvc_dir,
                                                        log_fname)
    assert fp == [os.path.join(data_row[2], data_row[1])]
    assert md5 == [data_row[0]]


def test_modify_last_update_time(tmpdir):
    """Test that the last_update time updates the file to something expected."""

    # timestamp 1
    tic = time.time()

    # create a config file
    config_path = os.path.join(str(tmpdir), config_fname)
    json.dump(dict(), open(config_path, 'w'))

    # update its timestamp
    modify_last_update_time(str(tmpdir))

    # timestamp 3
    toc = time.time()

    # now read the last modified update_time and verify that it is between the
    # last two timestamps
    last_update_str = json.load(open(config_path))['last_update']
    last_update = datetime.strptime(last_update_str, time_format).timestamp()

    # +/- 1s are for rounding error on timestamp()
    assert last_update + 1 > tic
    assert last_update - 1 < toc
