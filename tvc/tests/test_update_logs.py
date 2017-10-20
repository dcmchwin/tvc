"""Functions to to test the add_extension module."""

from argparse import Namespace
import pytest
from tvc.update_logs import main as update_logs
from tvc.add_extension import main as add_extension
from tvc.init_dir import _mk_logs as init_logs
from tvc.init_dir import _mk_config as init_cfg
from tvc.utils import modify_last_update_time, read_filepaths_and_md5_at_previous_update


@pytest.fixture(scope='module')
def args():
    """Dummy argparser Namespace object to spoof actual cl args."""
    args = Namespace()
    return args


def test_update_logs(args, tmpdir):
    """Check that logs are updated to include all files of tracked
    extension types."""
    # set up temporary path locations for test objects
    pd = tmpdir
    local_data = pd.mkdir('local_data')
    remote_data = pd.mkdir('remote_data')
    tvc = local_data.mkdir('.tvc')

    # ensure that config and log files exist
    args.remote = str(remote_data)
    init_cfg(args, str(tvc))
    init_logs(str(tvc))

    # create some local and remote data to track
    remote_data.join('data1.mp4').write('')
    remote_data.join('data2.h5').write('')
    local_data.join('data3.mat').write('')

    modify_last_update_time(str(tvc))

    # track only .mp4 and .mat diles
    for ext in ['.mp4', '.mat']:
        args.extension = ext
        add_extension(args, dot_tvc_dir=str(tvc))

    # update the logs
    update_logs(args, dot_tvc_dir=str(tvc))

    # verify updated log contents
    expected_local = set(['data3.mat'])
    expected_remote = set(['data1.mp4'])

    actual_local = \
        set(read_filepaths_and_md5_at_previous_update(str(tvc),
                                                      'local_log.csv')[0])
    actual_remote = \
        set(read_filepaths_and_md5_at_previous_update(str(tvc),
                                                      'remote_log.csv')[0])

    assert expected_local == actual_local
    assert expected_remote == actual_remote
