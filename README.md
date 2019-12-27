# Python Flask Api and MongoDB Boilerplate

Boilerplate from Python Flask Api with MongoDB

## Installation

### Virtualenv

Create a Python version 3.7 environment and activate it.

### Clone

Execute the following command to get the latest version of the project:

```terminal
$ git clone --recursive git@github.com:fndmiranda/flask-api.git flask-api
```

## Docker

### Create and start containers

```terminal
$ make start
```

### Install dependencies

Execute the following commands to install dependencies:

```terminal
$ pip install --upgrade pip
$ pip install -r requirements/development.txt
```

### Configure the application environment

Copy and edit the .env file as needed.

```terminal
$ cp .env.example .env
```

### Run application

```terminal
$ make runserver-dev
```

## Display registered routes.

Execute the following command to list all registered routes:

```terminal
$ make routes
```
