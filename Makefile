env:
  ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
  endif

start:
	docker-compose up -d

runserver-dev: env
	flask run

routes: env
	flask routes
