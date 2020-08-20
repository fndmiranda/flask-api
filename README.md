# Boilerplate of Python Flask Api, SQLAlchemy, migrations and OAuth2

This project simplifies the creation of a Python project with the Flask framework,
database migrations and authentication with OAuth2.

                                                                                                                        
## Installation

### Virtualenv

Create a Python version 3.7 environment and activate it.

### Clone

Execute the following command to get the latest version of the project:

```terminal
$ git clone --recursive git@github.com:fndmiranda/flask-api.git flask-api
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

### Run migrations

Execute the following command to upgrade to last revision:

```terminal
$ flask app migrate:run head
```

Or pass the version by parameter, see the example:
Below, we use `ae1` to refer to revision `ae1027a6acf`.
Tre migration will stop and let you know if more than one version starts with that prefix.

```terminal
$ flask app migrate:run ae1
```

Execute the following command to revert to an version:

```terminal
$ flask app migrate:downgrade -1
```

Relative identifiers may also be in terms of a specific revision.
For example, to upgrade to revision `ae1027a6acf` plus two additional steps:

```terminal
$ flask app migrate:revert ae10+2
```

Execute the following command to display the current revision for a database.

```terminal
$ flask app migrate:current
```

Execute the following command to list the history of migrations:

```terminal
$ flask app migrate:history
```

The --verbose option will show us full information about each revision:

```terminal
$ flask app migrate:history --verbose
```

### User

Execute the following command to create a new user:

```terminal
$ flask user user:create
```

Or pass the parameters to silent create.

```terminal
$ flask user user:create --name "YourName" --email youremail@domain.com --password yourpass
```

### OAuth2 authentication

Execute the following command to create a new OAuth2 client:

```terminal
$ flask auth client:create --scope=profile
```

The output will be something like.

```
New OAuth2 client created successfully.
Client ID: 8UTYVHgVBoNGj69pjS5e21Xa
Client secret: Cfa5VDPyHKJDxESc0ASKh8FmCbBEI4Fukp3jFxymnf0oxIcH
Grant type: ['password']
```

Optionally, the following arguments can be passed:

Argument | Accept | Default | Description
--- | --- | --- | ---
--name | string | APP_NAME constant | Name of the client.
--user | integer | None | A client is registered by a user (developer) on your website.
--uri | URI | None | Application URI.
--grant_type | [password, authorization_code] | password | Grant type, separated by comma
--redirect | URI | None | Where the user will be redirected after authorizing.
--response | string | code | Response type of solicitation.
--scope | string | None | Access level.


You can now request a token:

```http request
POST /oauth/token HTTP/1.1
Host: http://127.0.0.1:5000
Content-Type: application/x-www-form-urlencoded
Accept: application/json

grant_type=password&client_id=8UTYVHgVBoNGj69pjS5e21Xa&client_secret=Cfa5VDPyHKJDxESc0ASKh8FmCbBEI4Fukp3jFxymnf0oxIcH&username=email@domain.com&password=testpass&scope=profile
```

An example successful response:

```http request
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store
Pragma: no-cache

{
    "access_token": "7iON6iBSkLWwHQJB3OmxtUezgBdbwDpKNJyLrrf8PH",
    "expires_in": 864000,
    "refresh_token": "DashRD7mBqFEz5vUPiHzer8QsidtasqXkANcpxaUHtJnBMPM",
    "scope": "profile",
    "token_type": "Bearer"
}
```

### Run application

```terminal
$ flask run
```

## Display registered routes.

Execute the following command to list all registered routes:

```terminal
$ flask routes
```

## Security

If you discover any security related issues, please email fndmiranda@gmail.com instead of using the issue tracker.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
