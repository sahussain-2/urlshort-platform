.PHONY: help status lint format test

help:
	@echo "Available targets:"
	@echo "  make status  show git branch and working tree state"
	@echo "  make lint    check code style with ruff"
	@echo "  make format  format code with ruff"
	@echo "  make test    run the test suite"

status:
	@git branch --show-current
	@git status --short

lint:
	@ruff check .
	@ruff format --check .

format:
	@ruff format .

test:
	@python -m pytest -v
