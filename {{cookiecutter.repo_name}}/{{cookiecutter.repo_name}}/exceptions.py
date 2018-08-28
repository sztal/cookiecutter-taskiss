"""General exception classes."""


class AmbiguousMatchError(Exception):
    """Ambiguous match exception class.

    This exception should be raised in all cases when a key/name based
    search procedure over some set returns multiple matches in case this
    is considered an error.
    """
    @classmethod
    def from_matches(cls, matches, *args, key=None, **kwds):
        """Build exception from matches.

        Parameters
        ----------
        matches : Sequence
            Some sequence of matches.
        key : any
            Optional key. In most of cases this should be hashable object,
            but this is not enforced by the exception class.
        """
        if key is not None:
            message = f"'{key}' matches multiple targets (\'{', '.join(matches)}\')"
        else:
            message =  f"Matching mutliple targets (\'{', '.join(matches)}\'"
        return cls(message, *args, **kwds)
