test:
	python -m pytest --quiet tests/
.PHONY: test

format:
	black ./**/*.py --exclude env/
.PHONY: format

lint:
	flake8 .
	black ./**/*.py --check --exclude env/
.PHONY: lint
