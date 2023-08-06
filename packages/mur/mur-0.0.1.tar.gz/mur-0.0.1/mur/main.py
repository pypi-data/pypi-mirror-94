"""
"""

import click


PYTHON_VERSIONS_TUPLE = ('2', '3')
PYTHON_VERSION_CHOICES = click.Choice(PYTHON_VERSIONS_TUPLE, 
                                      case_sensitive=False)
PYTHON_DEFAULT_VERSION = '3'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """
    Main entrenca point for the cli.
    """
    pass


@murli.command()
def init():
    """
    Create a new Pyto project at current directory.
    """
    click.echo('Initialize Python project in given directory')


@murli.command('new', short_help='init a project')
@click.option('--python', 'python_version',
    required=False, 
    type=PYTHON_VERSION_CHOICES,
    default=PYTHON_DEFAULT_VERSION, 
    show_default=True,
    help='Specify Python version to use.')
@click.argument('path', 
    nargs=1, 
    required=True,
    type=click.Path(exists=False))
def new(python_version:int, path: click.Path):
    """
    Create a new Pyto project at PATH.
    """
    click.echo(f'Create new Python {python_version} project at {path}')
