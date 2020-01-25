import click
import subprocess
from flask import Blueprint

bp = Blueprint('app', __name__)


@bp.cli.command('migrate:history', context_settings={"ignore_unknown_options": True})
@click.option('--verbose/--no-shout', default=False)
@click.option('-r', default=False)
def migrate_history(verbose, r):
    """Show the history of migration."""
    args = ["alembic", "history"]

    if verbose:
        args.append('--verbose')

    if r:
        args.append('-r{}'.format(r))

    subprocess.run(args)


@bp.cli.command('migrate:run')
@click.argument('revision')
def migrate_run(revision):
    """Run the revision of migration."""
    args = ["alembic", "upgrade", revision]

    subprocess.run(args)


@bp.cli.command('migrate:revert')
@click.argument('revision')
def migrate_revert(revision):
    """Revert to a previous version."""
    args = ["alembic", "downgrade", revision]

    subprocess.run(args)


@bp.cli.command('migrate:current')
def migrate_current():
    """Display the current revision for a database."""
    args = ["alembic", "current"]

    subprocess.run(args)
