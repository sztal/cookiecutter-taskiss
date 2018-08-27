"""Command-line interface exception classes"""


class MalformedArgumentError(Exception):
    """Malformed command-line argument error."""

    def __init__(self, arg, *args, **kwds):
        """Initialization method."""
        message = f"Malformed argument {arg}"
        super().__init__(message, *args, **kwds)
