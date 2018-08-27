"""Path related utilities.

Attributes
----------
rx_file : re.Pattern
    Regexp for detecting file paths.
"""
import os
import re
from {{ cookiecutter.repo_name }}.config import cfg, MODE, ROOT_PATH

rx_file = re.compile(r"\.[a-z]*$", re.IGNORECASE)

# Base path getters -----------------------------------------------------------

def get_data_path(section, *args, **kwds):
    """Get path for the project data directory.

    Parameters
    ----------
    section : str
        Name of data section as defined in the config.
    *args :
        Path components.
    **kwds :
        Other arguments passed to `os.makedirs`.
    """
    dirpath = cfg.get(MODE, section)
    path = os.path.join(ROOT_PATH, dirpath, *args)
    return make_path(path, **kwds)

def get_rawdata_path(*args, **kwds):
    """Get rawdata project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_rawdata', *args, **kwds)

def get_persistence_path(*args, **kwds):
    """Get data persistence project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_persistence', *args, **kwds)

# -----------------------------------------------------------------------------

def is_file(path):
    """Tell if a path is a file path.

    In case of non-existent file paths the file extenstions
    serves as a file signature.

    Parameters
    ----------
    path : str
        Some path.
    """
    if os.path.exists(path):
        return os.path.isfile(path)
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
