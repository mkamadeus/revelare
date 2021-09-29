test:
	python -m pytest --quiet tests/
.PHONY: test

format:
	black ./**/*.py --exclude env/ --exclude venv/
.PHONY: format

lint:
	flake8 .
	black ./**/*.py --check --exclude env/ --exclude venv/
.PHONY: lint
