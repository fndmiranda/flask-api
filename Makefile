#!/bin/bash

env:
  ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
  endif

requirements-dev:
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

runserver-dev:
	@flask run

routes: env
	@flask routes

flake8:
	@flake8 --show-source

