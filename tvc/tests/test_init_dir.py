"""Test the init_dir module."""

from argparse import Namespace
from os import environ
from os.path import join, split
from py._path.local import LocalPath
import pytest
from tvc.init_dir import _mk_logs, _mk_tvc_dir, _mk_config


@pytest.fixture(scope='module')
def args():
    """Dummy argparser Namespace object to spoof actual cl args."""
    args = Namespace()
    # Set any legitimate file location as the remote path
    args.remote = environ['TEMP']
    return args


def get_file_contents_from_local_path(local_path: LocalPath) -> set:
    """Get the file names of the contents of the local_path object."""
    contents = set([split(str(lp))[-1] for lp in local_path.listdir()])
    print(type(local_path))
    return contents


def test_mk_tvc_dir(args, tmpdir):
    """Test that a .tvc folder is made."""
    _mk_tvc_dir(args, join(str(tmpdir), '.tvc'))
    actual_contents = get_file_contents_from_local_path(tmpdir)
    expected_contents = set(['.tvc'])
    assert actual_contents == expected_contents


def test_mk_config(args, tmpdir):
    """Assert that a config file is made in a .tvc dir."""
    _mk_config(args, str(tmpdir))
    actual_contents = get_file_contents_from_local_path(tmpdir)
    expected_contents = set(['config'])
    assert actual_contents == expected_contents


def test_mk_logs(tmpdir):
    """Test that log files of the correct name are made."""
    _mk_logs(str(tmpdir))
    actual_contents = get_file_contents_from_local_path(tmpdir)
    expected_contents = set(['remote_log.csv', 'local_log.csv'])
    assert actual_contents == expected_contents
