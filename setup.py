from setuptools import setup

setup(
    name='flask-app-commands',
    entry_points={
        'flask.commands': [
            # 'routes=app.commands:routes',
        ],
    }, install_requires=['click', 'flask']
)
