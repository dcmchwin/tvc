"""Functions to to test the add_extension module."""

from argparse import Namespace
import json
from os.path import join
import pytest
from tvc.add_extension import main as add_extension


@pytest.fixture(scope='module')
def args():
    """Dummy argparser Namespace object to spoof actual cl args."""
    args = Namespace()
    # Set any legitimate file location as the remote path
    args.extension = '.mp4'
    return args


def test_add_extension(args, tmpdir):
    """Test that the main function runs without error."""
    # create .tvc dir within test function
    dot_tvc_dir = str(tmpdir.mkdir('.tvc'))
    config = join(dot_tvc_dir, 'config')
    data = dict(tracked_extensions=[])
    with open(config, 'w') as f:
        json.dump(data, f)
    add_extension(args, join(str(tmpdir), '.tvc'))