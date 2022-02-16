.PHONY: install test dev clean doc check check-format format lint

DEV_BUILD_FLAG = .venv/DEV_BUILD_FLAG

install:
	python3 setup.py install

check: check-format test lint

test: $(DEV_BUILD_FLAG)
	.venv/bin/python -m unittest discover tests/
	.venv/bin/python -m doctest argparse_action/action.py

dev: $(DEV_BUILD_FLAG)

$(DEV_BUILD_FLAG):
	python -m venv .venv
	.venv/bin/pip install -e .
	.venv/bin/pip install sphinx black==22.1.0 pylint
	touch $(DEV_BUILD_FLAG)

clean:
	-rm -rf .venv
	-rm -rf docs/_build
	-rm -rf docs/articles/tutorial.rst

docs/articles/tutorial.rst: docs/examples/*/*
	python3 docs/examples/build.py > $@

doc: docs/articles/tutorial.rst $(DEV_BUILD_FLAG)
	.venv/bin/sphinx-build -b html docs docs/_build

format: $(DEV_BUILD_FLAG)
	.venv/bin/black argparse_action tests

check-format: $(DEV_BUILD_FLAG)
	.venv/bin/black --check argparse_action tests

lint: $(DEV_BUILD_FLAG)
	.venv/bin/pylint \
		--disable missing-function-docstring \
		--disable missing-class-docstring \
		--disable missing-module-docstring \
		--disable too-few-public-methods \
		argparse_action tests
