"""Command-line interface exception classes"""


class MalformedArgumentError(Exception):
    """Malformed command-line argument error."""

    @classmethod
    def from_arg(cls, arg, *args, **kwds):
        """Argument based constructor.

        Parameters
        ----------
        arg : str
            Argument.
        """
        return cls(f"Malformed argument {arg}", *args, **kwds)


class RepeatedArgumentError(Exception):
    """Repeated command-line argument error."""

    @classmethod
    def from_arg(cls, arg, values, *args, **kwds):
        """Argument and values based constructor.

        Parameters
        ----------
        arg : str
            Argument name.
        values : Iterable
            Argument values.
        """
        message = f"Argument '{arg}' is repeated with values: {', '.join(values)}"
        return cls(message, *args, **kwds)
