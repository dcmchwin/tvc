"""Functions for adding extensions to the list of tracked files.

This functions in this module facilitate adding extensions to the
config file in a .tvc directory.
"""

import json
import os


def main(args):
    """Add input extension to list of extensions in config file.

    Parameters
    ----------
    args: Namespace
        Command line arguments passed to the add_extension function"""

    config_path = os.path.join('.tvc', 'config')
    with open(config_path, 'r') as fin:
        data = json.load(fin)

    # Check that input argument starts with a full stop
    if args.extension[0] != '.':
        raise ValueError('{} not a valid file format - must start with a .'.
                         format(args.extension))

    data['tracked_extensions'].append(args.extension)

    with open(config_path, 'w') as fout:
        json.dump(data, fout)
