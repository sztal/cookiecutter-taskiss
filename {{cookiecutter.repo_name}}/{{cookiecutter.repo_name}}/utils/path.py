"""Path related utilities.

Attributes
----------
rx_file : re.Pattern
    Regexp for detecting file paths.
"""
import os
import re

rx_file = re.compile(r"\.[a-z]*$", re.IGNORECASE)

def is_file(path):
    """Tell if a path is a file path.

    Parameters
    ----------
    path : str
        Some path.
    """
    return bool(rx_file.search(path))

def make_path(*args, create_dir=True, **kwds):
    """Make path from fragments and create dir if does not exist.

    Parameters
    ----------
    *args :
        Path fragments.
    create_dir : bool
        Should directory be created if necessary.
    **kwds :
        Other arguments passed to `os.makedirs`.
    """
    path = os.path.join(*args)
    dirpath = os.path.dirname(path) if is_file(path) else path
    if create_dir and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True, **kwds)
    return path

def make_filepath(filename, dirpath, inc_if_taken=True, **kwds):
    """Make filepath for a given filename.

    This function allows for not overwriting existing files
    and incrementing filename counter instead.
    In such a case the filename must be a formattable string
    with a named placeholder `{n}`. Other named placeholder may be
    filled through `**kwds`.

    Parameters
    ----------
    filename : str
        File name.
    dirpath : str
        Directory path.
    inc_if_taken : bool
        Should file counter be used and incremented if a name is already taken.
    **kwds :
        Optional keyword arguments passed to the format string.
    """
    n = 0
    _filepath = os.path.join(dirpath, filename)
    filepath = _filepath
    while inc_if_taken:
        n += 1
        filepath = _filepath.format(n=n, **kwds)
        if not os.path.exists(filepath):
            break
    return filepath
