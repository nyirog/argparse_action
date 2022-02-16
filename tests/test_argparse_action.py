import unittest
import argparse
import contextlib
import io
import enum

import argparse_action


class ArgparseActionTest(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.action = argparse_action.Action(self.parser)

    def decorate(self, func, *aliases, **arg_options):
        wrapper = self.action.add(*aliases, **arg_options)
        wrapper(func)

    def parse_args(self, command_line):
        return self.parser.parse_args(command_line.split())

    def test_command_is_mandatory(self):
        self.decorate(simple_func)

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("")

    def test_command_has_to_be_a_registered_function(self):
        self.decorate(simple_func)

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("unknown")

    def test_function_name_is_valid_command(self):
        self.decorate(simple_func)
        namespace = self.parse_args("simple-func")

        self.assertIn("action", vars(namespace))

    def test_action_can_be_called_without_parameters(self):
        self.decorate(simple_func)
        namespace = self.parse_args("simple-func")

        self.assertEqual("simple", namespace.action(namespace))

    def test_aliases_are_valid_commands(self):
        self.decorate(simple_func, "alias")
        namespace = self.parse_args("alias")

        self.assertIn("action", vars(namespace))

    def test_function_parameter_is_converted_to_cli_argument(self):
        self.decorate(func_with_arg, "action")
        namespace = self.parse_args("action value")

        self.assertEqual("value", namespace.arg)

    def test_multiple_function_parameters_can_be_added(self):
        self.decorate(func_with_multiple_args, "action")
        namespace = self.parse_args("action first second")

        self.assertEqual("first", namespace.a)
        self.assertEqual("second", namespace.b)

    def test_action_can_be_called_with_cli_arguments(self):
        self.decorate(func_with_multiple_args, "action")
        namespace = self.parse_args("action first_ second")

        self.assertEqual("first_second", namespace.action(namespace))

    def test_cli_arguments_are_mandatory(self):
        self.decorate(func_with_multiple_args, "action")

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("action first")

    def test_cli_argument_follows_the_type_annotations(self):
        self.decorate(func_arg_with_annotation, "action")
        namespace = self.parse_args("action 42")

        self.assertEqual(42, namespace.number)

    def test_cli_argument_checks_the_type_annotations(self):
        self.decorate(func_arg_with_annotation, "action")

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("action invalid")

    def test_defaulted_arg_is_handled_as_cli_option(self):
        self.decorate(func_with_defaulted_arg, "action")
        namespace = self.parse_args("action --option any")

        self.assertEqual("any", namespace.option)

    def test_default_values_will_be_added_to_options(self):
        self.decorate(func_with_defaulted_arg, "action")
        namespace = self.parse_args("action")

        self.assertEqual("default", namespace.option)

    def test_cli_option_follows_the_type_annotations(self):
        self.decorate(func_defaulted_arg_with_annotation, "action")
        namespace = self.parse_args("action --option 42")

        self.assertEqual(42, namespace.option)

    def test_action_can_be_called_with_options(self):
        self.decorate(func_defaulted_arg_with_annotation, "action")
        namespace = self.parse_args("action --option 32")

        self.assertEqual(42, namespace.action(namespace))

    def test_cli_option_checks_the_type_annotations(self):
        self.decorate(func_defaulted_arg_with_annotation, "action")

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("action --option  invalid")

    def test_action_can_be_called_with_argumets_and_options(self):
        self.decorate(func_with_arg_and_defaulted_arg, "action")
        namespace = self.parse_args("action arg_ --option opt")
        self.assertEqual("arg_opt", namespace.action(namespace))

    def test_function_can_be_exposed_to_cli_without_its_name(self):
        self.parser = argparse.ArgumentParser()
        argparse_action.add_action(self.parser, func_with_arg_and_defaulted_arg)

        namespace = self.parse_args("one_ --option two")
        self.assertEqual("one_two", namespace.action(namespace))

    def test_bool_option_does_not_have_cli_values(self):
        self.decorate(func_arg_with_false_default_value, "action")
        namespace = self.parse_args("action --flag")

        self.assertTrue(namespace.flag)

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                self.parse_args("action --flag value")

    def test_bool_option_handles_default_value(self):
        self.decorate(func_arg_with_false_default_value, "action")
        namespace = self.parse_args("action")

        self.assertFalse(namespace.flag)

    def test_bool_option_negates_default_value(self):
        self.decorate(func_arg_with_true_default_value, "action")
        namespace = self.parse_args("action --flag")

        self.assertFalse(namespace.flag)

    def test_keyword_only_argument_is_handled(self):
        self.decorate(func_with_keyword_only_arg, "action")
        namespace = self.parse_args("action value")

        self.assertEqual("value", namespace.action(namespace))

    def test_defaulted_keyword_only_argument_will_be_a_cli_option(self):
        self.decorate(func_with_defaulted_keyword_only_arg, "action")

        namespace = self.parse_args("action")
        self.assertEqual("default", namespace.action(namespace))

        namespace = self.parse_args("action --option value")
        self.assertEqual("value", namespace.action(namespace))

    def test_varg_will_be_nargs_star_cli_argument(self):
        self.decorate(func_with_varg, "action")

        namespace = self.parse_args("action a b c")
        self.assertEqual(("a", "b", "c"), namespace.action(namespace))

        namespace = self.parse_args("action")
        self.assertEqual((), namespace.action(namespace))

    def test_arg_can_be_exposed_with_varg(self):
        self.decorate(func_with_arg_and_varg, "action")

        namespace = self.parse_args("action egg. spam spamspam")
        self.assertEqual(["egg.spam", "egg.spamspam"], namespace.action(namespace))

    def test_varg_can_be_exposed_defaulted_value(self):
        self.decorate(func_with_varg_and_defaulted_arg, "action")

        namespace = self.parse_args("action egg. eggegg.")
        self.assertEqual(["egg.spam", "eggegg.spam"], namespace.action(namespace))

        namespace = self.parse_args("action egg. eggegg. --option ham")
        self.assertEqual(["egg.ham", "eggegg.ham"], namespace.action(namespace))

    def test_arg_varg_and_defaulted_value_can_be_exposed_together(self):
        self.decorate(func_with_arg_varg_and_defaulted_arg, "action")

        namespace = self.parse_args("action ham. egg. eggegg.")
        self.assertEqual(
            ["ham.egg.spam", "ham.eggegg.spam"], namespace.action(namespace)
        )

        namespace = self.parse_args("action ham. egg. eggegg. --option cheese")
        self.assertEqual(
            ["ham.egg.cheese", "ham.eggegg.cheese"], namespace.action(namespace)
        )

    def test_single_character_defaulted_argument_will_be_short_option(self):
        self.decorate(func_with_defaulted_short_arg, "action")
        namespace = self.parse_args("action -o option")
        self.assertEqual("option", namespace.o)

    def test_varg_annotation_is_handled_by_argparse(self):
        self.decorate(func_varg_with_annotation, "action")

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                namespace = self.parse_args("action invalid")

        namespace = self.parse_args("action 13 26")
        self.assertEqual([13, 26], namespace.args)
        self.assertEqual(39, namespace.action(namespace))

    def test_choices_are_created_from_enum_annotation(self):
        self.decorate(func_with_enum_arg_annotation, "action")

        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit):
                namespace = self.parse_args("action unknown")

        namespace = self.parse_args("action info")
        self.assertEqual("info", namespace.level)
        self.assertEqual(Level.info, namespace.action(namespace))

    def test_argparse_option_can_be_injected(self):
        self.decorate(func_with_defaulted_int_arg, "action", n={"action": "count"})

        namespace = self.parse_args("action")
        self.assertEqual(0, namespace.n)

        namespace = self.parse_args("action -nn")
        self.assertEqual(2, namespace.n)

    def test_handle_underscore_in_parameter(self):
        self.decorate(func_with_underscore_in_param, "action")

        namespace = self.parse_args("action underscore_param")

        self.assertEqual("underscore_param", getattr(namespace, "my-param"))
        self.assertEqual("underscore_param", namespace.action(namespace))

    def test_handle_underscore_in_vargs(self):
        self.decorate(func_with_underscore_in_vargs, "action")

        namespace = self.parse_args("action p_1 p_2")

        self.assertEqual(["p_1", "p_2"], getattr(namespace, "my-params"))
        self.assertEqual("p_1:p_2", namespace.action(namespace))

    def test_handle_underscore_in_kwargs(self):
        self.decorate(func_with_underscore_in_kwargs, "action")

        namespace = self.parse_args("action --kw-arg other")

        self.assertEqual("other", getattr(namespace, "kw_arg"))
        self.assertEqual("other", namespace.action(namespace))

    def test_handle_underscore_in_defaulted_arg(self):
        self.decorate(func_with_underscore_in_defaulted_arg, "action")

        namespace = self.parse_args("action --default-param other")

        self.assertEqual("other", getattr(namespace, "default_param"))
        self.assertEqual("other", namespace.action(namespace))


def simple_func():
    return "simple"


def func_with_arg(arg):
    return arg


def func_with_multiple_args(a, b):
    return a + b


def func_arg_with_annotation(number: int):
    return number


def func_with_defaulted_arg(option="default"):
    return arg


def func_with_arg_and_defaulted_arg(arg, option="default"):
    return arg + option


def func_defaulted_arg_with_annotation(option: int = 10):
    return option + 10


def func_arg_with_false_default_value(flag=False):
    return flag


def func_arg_with_true_default_value(flag=True):
    return flag


def func_with_keyword_only_arg(*, arg):
    return arg


def func_with_defaulted_keyword_only_arg(*, option="default"):
    return option


def func_with_varg(*args):
    return args


def func_varg_with_annotation(*args: int):
    return sum(args)


def func_with_arg_and_varg(arg, *args):
    return [arg + s for s in args]


def func_with_varg_and_defaulted_arg(*args, option="spam"):
    return [arg + option for arg in args]


def func_with_arg_varg_and_defaulted_arg(arg, *args, option="spam"):
    return [arg + a + option for a in args]


def func_with_defaulted_short_arg(o="default"):
    return o


class Level(enum.Enum):
    debug = enum.auto()
    info = enum.auto()
    error = enum.auto()


def func_with_enum_arg_annotation(level: Level):
    return level


def func_with_defaulted_int_arg(n=0):
    return n


def func_with_underscore_in_param(my_param):
    return my_param


def func_with_underscore_in_vargs(*my_params):
    return ":".join(my_params)


def func_with_underscore_in_kwargs(*, kw_arg="DEFAULT"):
    return kw_arg


def func_with_underscore_in_defaulted_arg(default_param="DEFAULT"):
    return default_param
