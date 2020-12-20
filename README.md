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

namespace = pasrer.parse_args()
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
python3 setup.py install
```

## Testing

```
make test
```

## Documentation

Documentation can be build with the `doc` make target:

```
make doc
```

Online version can be read at [readthedocs.org](https://argparse-action.readthedocs.io/en/latest/index.html).
