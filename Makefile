COMPOSE := $(shell which docker-compose)
ifeq ($(COMPOSE),)
	COMPOSE := docker compose
endif

run:
	${COMPOSE} up

build:
	${COMPOSE} up --build

stop:
	${COMPOSE} down

# Poetry commands

update-deps:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
venv:
	poetry config virtualenvs.create $(PY_VENV)
