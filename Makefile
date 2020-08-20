#!/bin/bash

env:
  ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
  endif

requirements-dev:
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

runserver-dev: env
	@flask run

runserver: env
	@gunicorn run:app -t 120

create-user:
	@flask user user:create

create-user-admin:
	@flask user user:create --admin

routes: env
	@flask routes

flake8:
	@flake8 --show-source

