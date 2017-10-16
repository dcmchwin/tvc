"""Module to update logs to agree with list of tracked extensions."""

def main(args):
    raise NotImplementedError

def _mk_hash_log(folder):
    """Get csv mapping hash files."""
    raise NotImplementedError


def md5(fname):
    """Get md5 hash of file."""
    hasher = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hasher.update(chunk)
    return hasher.hexdigest()