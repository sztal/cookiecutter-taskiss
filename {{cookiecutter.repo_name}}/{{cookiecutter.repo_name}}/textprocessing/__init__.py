"""Module for processing and manipulation of text data."""
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
    if isinstance(salt, str):
        string += salt
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def sectionize(parts):
    """Join parts of the text after splitting into sections with headings.

    This function assumes that a text was splitted at section headings,
    so every list element after the first one is a heading-section pair.
    This assumption is used to join sections with their corresponding headings.

    Parameters
    ----------
    parts : list of str
        List of text parts.
    """
    if len(parts) <= 1:
        return parts
    sections = parts[:1] \
        + [ " ".join(parts[i:i+2]) for i in range(1, len(parts), 2) ]
    return sections

def strip(x):
    """Strip a string.

    Parameters
    ----------
    x : any
        A str object which is to be stripped. Anything else is returned as is.
    """
    if isinstance(x, str):
        return x.strip()
    return x

def split(x, divider):
    """Split a string.

    Parameters
    ----------
    x : any
        A str object to be split. Anything else is returned as is.
    divider : str
        Divider string.
    """
    if isinstance(x, str):
        return x.split(divider)
    return x
