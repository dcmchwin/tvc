from tvc.init_dir import _mk_logs
from os.path import abspath, join, split
import pytest


@pytest.fixture(scope='module')
def tests_data_dir():
    tests_dir = split(abspath(__file__))[0]
    return join(tests_dir, 'data')


def test_mk_logs(tests_data_dir):
    _mk_logs(tests_data_dir)
