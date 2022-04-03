import collections.abc
import argparse
import inspect
import itertools
import typing
import types
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
        self._parsers = parser.add_subparsers(dest="command", metavar="command")
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
            name=_conv_to_cli_name(func.__name__), help=func.__doc__, aliases=aliases
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

        parser.add_argument(_conv_to_cli_option(name, param), **options)

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
            _get_action(param),
        )
    )


def _get_bool_options(param):
    action = "store_false" if param.default else "store_true"

    return dict(default=param.default, action=action)


def _get_annotation(param):
    if param.annotation == param.empty or _is_enum(param.annotation):
        return

    if seq_type := _is_sequence(param.default) and _is_typed_sequence(param.annotation):
        if not _is_typed_enum_sequence(param.annotation):
            yield "type", seq_type

    else:
        yield "type", param.annotation


def _get_default(param):
    if param.default == param.empty:
        return

    if _is_enum(param.annotation):
        yield "default", param.default.name

    elif _is_sequence(param.default):
        yield "default", []

    else:
        yield "default", param.default

    yield "help", "default: %(default)s"


def _get_nargs(param):
    if param.kind == param.VAR_POSITIONAL:
        yield "nargs", "*"


def _get_choices(param):
    if enum_annotation := _is_enum(param.annotation):
        yield "choices", list(enum_annotation.__members__)

    elif enum_annotation := _is_typed_enum_sequence(param.annotation):
        yield "choices", list(enum_annotation.__members__)


def _get_action(param):
    if not _is_sequence(param.default):
        return

    yield "action", "append"


def _is_enum(annotation):
    if inspect.isclass(annotation) and issubclass(annotation, enum.Enum):
        return annotation

    return False


def _is_bool(param):
    return isinstance(param.default, bool)


def _wrap_action(func, sig):
    def action(namespace):
        args = [
            _get_namespace_var(
                namespace,
                _conv_to_cli_name(name) if param.default == param.empty else name,
                param,
            )
            for name, param in sig.parameters.items()
            if param.kind not in {param.VAR_POSITIONAL, param.KEYWORD_ONLY}
        ]

        varg_name = _get_varg_name(sig)

        if varg_name is not None:
            varg = _get_namespace_var(
                namespace, _conv_to_cli_name(varg_name), sig.parameters[varg_name]
            )
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

    if enum_annotation := _is_enum(param.annotation):
        if _is_sequence(var):
            var = [enum_annotation[item] for item in var]
        else:
            var = param.annotation[var]
    elif enum_annotation := _is_typed_enum_sequence(param.annotation):
        var = [enum_annotation[item] for item in var]

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


def _is_sequence(value):
    """
    Check that `value` is a sequence but not str.
    """
    return not isinstance(value, str) and isinstance(value, collections.abc.Sequence)


def _is_typed_sequence(annotation):
    #  pylint: disable=protected-access
    if (
        isinstance(annotation, (types.GenericAlias, typing._GenericAlias))
        and issubclass(annotation.__origin__, collections.abc.Sequence)
        and len(annotation.__args__) == 1
    ):
        return annotation.__args__[0]

    return False


def _is_typed_enum_sequence(annotation):
    if sequence_type := _is_typed_sequence(annotation):
        return _is_enum(sequence_type)

    return False
