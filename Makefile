# Docker compose commands

run:
	docker-compose up

build:
	docker-compose up --build


# Poetry commands

update-deps:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
venv:
	poetry config virtualenvs.create $(PY_VENV)