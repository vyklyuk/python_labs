export PYTHONPATH=$(shell pwd)/src

db:
	docker run -e POSTGRES_PASSWORD=123456 -p 5432:5432 postgres

apply-migrations:
	$(MAKE) -C src apply-migrations

run:
	FLASK_APP=src/app.py FLASK_ENV=development flask run

gunicorn:
	gunicorn -b 127.0.0.1:5000 app:app