"""CLI: DB submodule for MongoDB / Mongoengine management."""
import click


@click.group()
def mongo():
    """MongoDB / Mongoengine management inteface."""
    pass
