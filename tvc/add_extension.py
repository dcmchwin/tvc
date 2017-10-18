"""Add extensions to list."""
import json
import os


def main(args):
    """Add input extension to list of extensions in config file."""

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
