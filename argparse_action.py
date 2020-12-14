import argparse
import inspect


class Action:
    """
    >>> import argparse
    >>> parser = argparse.ArgumentParser()
    >>> action = Action(parser)
    >>> @action.add()
    ... def concatenate(a, b):
    ...     return a + b
    >>> namespace = parser.parse_args("concatenate one_ two ".split())
    >>> namespace.action(namespace)
    'one_two'
    """

    def __init__(self, parser: argparse.ArgumentParser):
        self._parsers = parser.add_subparsers(dest='command', metavar='command')
        self._parsers.required = True

    def add(self, *aliases):
        """
        Register the decoreated function into command subparsers with the name
        of the function. The arguments and options are set by ``add_action``.

        Arbitrary number of aliases can be specified via ``*aliases`` parameter.
        """

        def wrapper(func):
            parser = self._add_parser(func, aliases)
            add_action(parser, func)

            return func

        return wrapper

    def _add_parser(self, func, aliases):
        return self._parsers.add_parser(
            name=_conv_to_cli_name(func.__name__),
            help=func.__doc__,
            aliases=aliases
        )



def add_action(parser, func: callable):
    """
    Registers arguments and options into ``parser`` from the signature of
    ``func``. A function wrapper is created from the ``func`` and stored in the
    ``action`` field of the parsed namespace. The ``action`` can be called with
    the namespace to execute the ``func`` with the cli input.

    The type annotation of the parameters are forced to the cli arguments.
    The used type annotations have to accept str input.

    The arguments with default values will be handled as cli options.

    Bool default values will be handled as flags ("store_true", "store_false").
    The bool option negates its default value.

    *args parameters will be handled as nargs='*' arguments.
    """
    sig = _add_arguments(parser, func)
    action = _wrap_action(func, sig)
    parser.set_defaults(action=action)


def _add_arguments(parser, func):
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if param.kind == param.VAR_POSITIONAL:
            parser.add_argument(name, nargs="*")

        elif param.default == param.empty:
            parser.add_argument(name, type=_get_annotation(param))

        else:
            _add_option(parser, name, param)

    return sig


def _add_option(parser, name, param):
    if _is_bool(param):
        _add_bool_option(parser, name, param)
    else:
        _add_normal_option(parser, name, param)


def _add_bool_option(parser, name, param):
    action = "store_false" if param.default else "store_true"

    parser.add_argument(
        _conv_to_cli_option(name),
        default=param.default,
        action=action
    )


def _add_normal_option(parser, name, param):
    parser.add_argument(
        _conv_to_cli_option(name),
        type=_get_annotation(param),
        default=_get_default(param)
    )


def _get_annotation(param):
    return param.annotation if param.annotation != param.empty else None


def _get_default(param):
    return param.default if param.default != param.empty else None


def _is_bool(param):
    return isinstance(param.default, bool)


def _wrap_action(func, sig):
    def action(namespace):
        namespace_vars = vars(namespace)

        args = [
            namespace_vars[name]
            for name, param in sig.parameters.items()
            if param.kind not in {param.VAR_POSITIONAL, param.KEYWORD_ONLY}
        ]

        varg_name = _get_varg_name(sig)

        if varg_name is not None:
            args.extend(namespace_vars[varg_name])

        kwargs = {
            name: namespace_vars[name]
            for name, param in sig.parameters.items()
            if param.kind == param.KEYWORD_ONLY
        }

        return func(*args, **kwargs)

    return action


def _get_varg_name(sig):
    names = (
        name
        for name, param in sig.parameters.items()
        if param.kind == param.VAR_POSITIONAL
    )

    return next(names, None)


def _conv_to_cli_option(name):
    return "--" + _conv_to_cli_name(name)


def _conv_to_cli_name(name):
    return name.replace("_", "-")
