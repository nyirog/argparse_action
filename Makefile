.PHONY: install test dev clean doc

DEV_BUILD_FLAG = .venv/DEV_BUILD_FLAG

install:
	python3 setup.py install

test: $(DEV_BUILD_FLAG)
	.venv/bin/python -m unittest discover tests/
	.venv/bin/python -m doctest argparse_action.py

dev: $(DEV_BUILD_FLAG)

$(DEV_BUILD_FLAG):
	python -m venv .venv
	.venv/bin/pip install -e .
	.venv/bin/pip install sphinx
	touch $(DEV_BUILD_FLAG)

clean:
	-rm -rf .venv
	-rm -rf docs/_build
	-rm -rf docs/articles/tutorial.rst

docs/articles/tutorial.rst: docs/examples/*/*
	python3 docs/examples/build.py > $@

doc: docs/articles/tutorial.rst $(DEV_BUILD_FLAG)
	.venv/bin/sphinx-build -b html docs docs/_build
