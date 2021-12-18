import argparse
import inspect
import itertools
import enum


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

    def add(self, *aliases, **arg_options):
        """
        Register the decoreated function into command subparsers with the name
        of the function. The arguments and options are set by ``add_action``.

        Arbitrary number of aliases can be specified via ``*aliases`` parameter.
        """

        def wrapper(func):
            parser = self._add_parser(func, aliases)
            add_action(parser, func, **arg_options)

            return func

        return wrapper

    def _add_parser(self, func, aliases):
        return self._parsers.add_parser(
            name=_conv_to_cli_name(func.__name__),
            help=func.__doc__,
            aliases=aliases
        )



def add_action(parser, func: callable, **arg_options):
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

    Keyword arguments of ``add_action`` are handled as extra argparse options
    of the parsed arguments of ``func``. The name of the keyword argument has to
    refer to a ``func`` argument which will be extended. The keyword argument
    of ``add_action`` only extend the argparse options of the parsed ``func``
    arguments the same rules apply to the extended arguments as the normal
    ``func`` arguments.
    """
    sig = _add_arguments(parser, func, arg_options)
    action = _wrap_action(func, sig)
    parser.set_defaults(action=action)


def _add_arguments(parser, func, arg_options):
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        options = _get_options(param)
        options.update(arg_options.get(name, {}))

        parser.add_argument(
            _conv_to_cli_option(name, param),
            **options
        )

    return sig


def _get_options(param):
    if _is_bool(param):
        return _get_bool_options(param)

    return dict(
        itertools.chain(
            _get_annotation(param),
            _get_nargs(param),
            _get_default(param),
            _get_choices(param),
        )
    )


def _get_bool_options(param):
    action = "store_false" if param.default else "store_true"

    return dict(
        default=param.default,
        action=action
    )


def _get_annotation(param):
    if param.annotation == param.empty or _is_enum(param):
        return

    yield "type", param.annotation


def _get_default(param):
    if param.default == param.empty:
        return

    elif _is_enum(param):
        yield "default", param.default.name

    else:
        yield "default", param.default

    yield "help", "default: %(default)s"


def _get_nargs(param):
    if param.kind == param.VAR_POSITIONAL:
        yield "nargs", "*"

    return


def _get_choices(param):
    if _is_enum(param):
        yield "choices", list(param.annotation.__members__)

    return


def _is_enum(param):
    return inspect.isclass(param.annotation) and issubclass(param.annotation, enum.Enum)

def _is_bool(param):
    return isinstance(param.default, bool)


def _wrap_action(func, sig):
    def action(namespace):
        namespace_vars = vars(namespace)

        args = [
            _get_namespace_var(
                namespace,
                _conv_to_cli_name(name) if param.default == param.empty else name,
                param
            )

            for name, param in sig.parameters.items()
            if param.kind not in {param.VAR_POSITIONAL, param.KEYWORD_ONLY}
        ]

        varg_name = _get_varg_name(sig)

        if varg_name is not None:
            varg = _get_namespace_var(namespace, _conv_to_cli_name(varg_name), sig.parameters[varg_name])
            args.extend(varg)

        kwargs = {
            name: _get_namespace_var(namespace, name, param)
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


def _get_namespace_var(namespace, name, param):
    var = getattr(namespace, name)

    if _is_enum(param):
        var = param.annotation[var]

    return var


def _conv_to_cli_option(name, param):
    if param.default == param.empty:
        prefix = ""
    elif len(name) == 1:
        prefix = "-"
    else:
        prefix = "--"

    return prefix + _conv_to_cli_name(name)


def _conv_to_cli_name(name):
    return name.replace("_", "-")
