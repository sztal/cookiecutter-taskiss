"""_Taskiss_ exception classes."""

class AmbiguousTaskArgumentsError(Exception):
    """Embiguous task arguments error class."""

    def __init__(self, ambiguous, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        ambiguous : dict
            Dict with keys and ambiguous values.
        """
        message = "Ambiguous task arguments for:\n\t{}".format(
            "\n\t".join([ "{} => {}".format(k, v) for k, v in ambiguous.items() ])
        )
        super().__init__(message, *args, **kwds)
