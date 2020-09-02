from setuptools import setup

setup(
    name='flask-app-commands',
    entry_points={
        'flask.commands': [],
    }, install_requires=['click', 'flask']
)
