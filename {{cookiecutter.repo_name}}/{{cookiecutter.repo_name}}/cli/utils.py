"""Command-line interface utilities."""

def eager_callback(callback, *args, **kwds):
    """Warpper for executing callbacks of eager options.

    Parameters
    ----------
    ctx : :py:class:`click.Context`
        Context object.
    value : any
        Value.
    *args :
        Positional arguments passed to the callback.
    **kwds :
        Keyword arguments passed to the callback.
    """
    def callback_wrapper(ctx, param, value):
        """Wrapped callback."""
        if not value or ctx.resilient_parsing:
            return
        callback(*args, **kwds)
        ctx.exit()
    return callback_wrapper
