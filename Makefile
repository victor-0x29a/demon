include .env
export

install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/dev.txt

dev:
	export REDIS_OM_URL=redis://default:$(redis_pwd)@$(redis_host):$(redis_port)
	uvicorn main:app --reload

test:
	pytest