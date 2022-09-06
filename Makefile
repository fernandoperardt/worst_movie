.PHONY: dev
dev:
		FLASK_APP=./app/app.py FLASK_DEBUG=0 flask run

test:
		PYTHONPATH=. pytest -v -s -p no:warnings -vv

migrate-up:
		FLASK_APP=./app/app.py flask db upgrade

migrate-down:
		FLASK_APP=./app/app.py flask db downgrade

migrate:
		FLASK_APP=./app/app.py flask db migrate
