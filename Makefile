.PHONY: install test dev clean doc

install:
	python3 setup.py install

test:
	python3 -m unittest discover tests/
	python3 -m doctest argparse_action.py

dev:
	virtualenv .venv
	.venv/bin/pip install sphinx

clean:
	-rm -rf .venv
	-rm -rf doc/_build

doc: dev
	.venv/bin/sphinx-build -b html doc doc/_build
