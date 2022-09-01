.PHONY: dev
dev:
		FLASK_APP=./app/app.py FLASK_DEBUG=1 flask run

test:
		PYTHONPATH=. pytest --testdox -s
