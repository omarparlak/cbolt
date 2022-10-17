install:
	@poetry install

update:
	@poetry update

migrate:
	@poetry run python src/manage.py makemigrations
	@poetry run python src/manage.py migrate

seed:
	@poetry run python src/manage.py seed_database

build: install migrate seed

killdb:
	@rm -f src/db.sqlite3

wipe: killdb migrate seed

run:
	@poetry run python src/manage.py runserver 0.0.0.0:8080

shell:
	@poetry run python src/manage.py shell

format:
	@poetry run black src
	@poetry run flake8 src

test:
	@poetry run python src/manage.py test messageboard.tests

stats:
	@poetry run python stats.py
