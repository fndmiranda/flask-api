import click
import subprocess
from flask import Blueprint
from user.services import UserService

bp = Blueprint('user', __name__)


@bp.cli.command('user:create')
@click.option('--email', default=False)
@click.option('--name', default=False)
@click.option('--password', default=False)
def user_create(email, name, password):
    """Create a new user."""

    if email is False:
        email = click.prompt('Enter the email')

    if name is False:
        name = click.prompt('Enter the name')

    if password is False:
        password = click.prompt('Enter the password', hide_input=True)

    user = UserService().create({
        'email': email,
        'name': name,
        'password': password
    })

    click.echo(click.style('New user created successfully.', fg='green'))
    click.echo(click.style('ID: ', fg='yellow') + str(user.id))
    click.echo(click.style('Name: ', fg='yellow') + user.name)
    click.echo(click.style('Email: ', fg='yellow') + user.email)
