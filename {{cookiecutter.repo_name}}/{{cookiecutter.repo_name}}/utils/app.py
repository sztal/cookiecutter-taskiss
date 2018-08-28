"""Application specific utilities."""
from {{ cookiecutter.repo_name }}.config import cfg, MODE, ROOT_PATH


# Base path getter ------------------------------------------------------------

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
    return get_data_path('path_data_rawdata', *args, **kwds)

def get_persistence_path(*args, **kwds):
    """Get data persistence project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_data_persistence', *args, **kwds)

# -----------------------------------------------------------------------------
