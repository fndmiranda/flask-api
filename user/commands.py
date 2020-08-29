import click
from flask import Blueprint
from sqlalchemy import exc
from user.services import UserService

bp = Blueprint('user', __name__)


@bp.cli.command('user:create')
@click.option('--email', default=False)
@click.option('--name', default=False)
@click.option('--password', default=False)
@click.option('--admin/--no-admin', default=False)
def user_create(email, name, password, admin):
    """Create a new user."""

    if email is False:
        email = click.prompt('Enter the email')

    if name is False:
        name = click.prompt('Enter the name')

    if password is False:
        password = click.prompt('Enter the password', hide_input=True)

    try:
        user = UserService().create({
            'email': email,
            'name': name,
            'password': password,
            'is_admin': admin,
        })
    except exc.SQLAlchemyError as e:
        click.echo(click.style(str(e), fg='red'))
        exit()

    click.echo(click.style('New user created successfully.', fg='green'))
    click.echo(click.style('ID: ', fg='yellow') + str(user.id))
    click.echo(click.style('Name: ', fg='yellow') + user.name)
    click.echo(click.style('Email: ', fg='yellow') + user.email)
    click.echo(click.style('Admin: ', fg='yellow') + ('yes' if user.is_admin else 'no'))
