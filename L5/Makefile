export ENV_BIN=env/bin
export PYTHONPATH=$(shell pwd)
export DATABASE_CONTAINER_NAME=lab5-db

db-up:
	$(MAKE) apply-migrations

apply-migrations:
	alembic upgrade head

db-down:
	docker rm -f $(DATABASE_CONTAINER_NAME) || true

run-with-flask: export FLASK_APP=lab5/app.py
run-with-flask: export FLASK_ENV=development
run-with-flask:
	flask run

run-with-gunicorn: db-up
	gunicorn -b 127.0.0.1:5000 --log-level DEBUG lab5.app:app
