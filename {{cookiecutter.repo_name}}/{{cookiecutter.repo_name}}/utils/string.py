"""Utilities for processing strings and text data."""
import hashlib


def hash_string(string, salt=None):
    """Get MD5 hash from a string.

    Parameters
    ----------
    string : str
        Some string.
    salt : str, False or None
        Optional salt added to the string for additional obfuscation.
    """
    if salt is not None:
        string += salt
    return hashlib.md5(string.encode('utf-8')).hexdigest()
