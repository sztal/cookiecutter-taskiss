"""Utility functions for running tests."""

def make_cli_args(*args):
    """Prepare args for invoking the CLI."""
    return [ (x.strip() if isinstance(x, str) else x) for x in args if x ]
