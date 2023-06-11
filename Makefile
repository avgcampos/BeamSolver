#Makefile
.PHONY: install format lint test

install:
	pip install -r requirements.txt

format:
	black beamsolver
	isort beamsolver

lint:
	black beamsolver --check
	isort beamsolver --check
	flake8 beamsolver
	interrogate -vv beamsolver

test:
	pytest -v