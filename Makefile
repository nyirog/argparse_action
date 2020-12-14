.PHONY: install test

install:
	python3 setup.py install

test:
	python3 -m unittest discover tests/
	python3 -m doctest argparse_action.py
