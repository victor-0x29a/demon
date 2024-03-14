install:
	pip install -r requirements/base.txt

dev:
	uvicorn main:app --reload