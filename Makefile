include .env
export

install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/dev.txt

dev:
	uvicorn main:app --reload

test:
	export FASTAPI_ENV=test && pytest