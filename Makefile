# Makefile

export UID := $(shell id -u)
export GID := $(shell id -g)

COMPOSE = UID=$(UID) GID=$(GID) docker compose

.PHONY: up down build logs ps stop run exec shell create-app

up:
	$(COMPOSE) up

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) build --no-cache

logs:
	$(COMPOSE) logs -f

exec-web:
	$(COMPOSE) exec web bash

lint:
	$(COMPOSE) run --rm web flake8

ps:
	$(COMPOSE) ps

stop:
	$(COMPOSE) stop

run:
	$(COMPOSE) run --rm web $(CMD)

exec:
	$(COMPOSE) exec web $(CMD)

shell:
	$(COMPOSE) exec web sh

create-app:
	$(COMPOSE) run --rm web python manage.py startapp $(APP)

makemigrations:
	$(COMPOSE) run --rm web python manage.py makemigrations

migrate:
	$(COMPOSE) run --rm web python manage.py migrate

csu:
	$(COMPOSE) run --rm web python manage.py createsuperuser

test:
	$(COMPOSE) run --rm web python manage.py test
