-include .env
export

db.run:
	@docker-compose up -d db

parse.run:
	@docker-compose build
	@docker-compose up -d

stop:
	@docker-compose stop -t 1

clean:
	@docker-compose down

lint:
	@mypy backend
	@flake8 backend

db.create:
	@python -m backend.models

run:
	@python -m backend

parse:
	@python -m backend.parser.hh

db.makemigrations:
	@alembic revision --autogenerate -m "${message}"

db.migrate:
	@alembic upgrade head

alembic:
	@alembic ${command}
