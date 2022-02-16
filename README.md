[![Makefile CI](https://github.com/nyirog/argparse_action/actions/workflows/makefile.yml/badge.svg?branch=master)](https://github.com/nyirog/argparse_action/actions/workflows/makefile.yml)
# argparse_action

`argparse_action` aims to be a minimalistic extension of `argparse` and creates
cli options from the function signature given by `inspect.signature`.

```python
import argparse
import argparse_action

parser = argparse.ArgumentParser()
action = argparse_action.Action(parser)

@action.add("e")
def echo(word, upper=False):
    print(word.upper() if upper else word)

namespace = parser.parse_args()
namespace.action(namespace)
```

Asumes that the code above is saved as `my_script.py`:

```
$ python3 my_script.py echo hello
hello

$ python3 my_script.py e hello
hello

$ python3 my_script.py echo --upper hello
HELLO
```

## Installation

```
pip install argparse_action
```

## Configuration

```
make dev
```

## CI check

The `check` make target collects the targets which are run by the CI server.

```sh
make check
```

### Testing

The `test` target requires a virtulenv where `argparse_action` is installed.
The `dev` target creates that virtualenv under `.venv` directory.

```
make test
```

### Formatting

The argparse_action project is formatted with `black`. The CI check invokes the
`check-format` target to ensure that the python files are formatted with
`black`.

```sh
make check-format
```

`black` can be run with the `format` make target.

```sh
make format
```

### Linter

The `lint` target runs `pylint` over the argparse_action project.

```sh
make lint
```

## Documentation

Documentation can be build with the `doc` make target. To ensure the documentation build
tools the `make dev` has to be executed once before `make doc`.

```
make doc
```

Online version can be read at [readthedocs.org](https://argparse-action.readthedocs.io/en/latest/index.html).
