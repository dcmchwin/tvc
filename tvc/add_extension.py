"""Functions for adding extensions to the list of tracked files.

This functions in this module facilitate adding extensions to the
config file in a .tvc directory.
"""

import json
import os
from tvc.utils import get_config_data


def main(args, dot_tvc_dir=None):
    """Add input extension to list of extensions in config file.

    Parameters
    ----------
    args: Namespace
        Command line arguments passed to the add_extension function
    dot_tvc_dir: str
        path to .tvc directory
    """
    if dot_tvc_dir is None:
        dot_tvc_dir = os.path.abspath('.tvc')

    data = get_config_data(dot_tvc_dir)

    # Check that input argument starts with a full stop
    if args.extension[0] != '.':
        raise ValueError('{} not a valid file format - must start with a .'.
                         format(args.extension))

    data['tracked_extensions'].append(args.extension)

    config_path = os.path.join(dot_tvc_dir, 'config')
    with open(config_path, 'w') as fout:
        json.dump(data, fout)
