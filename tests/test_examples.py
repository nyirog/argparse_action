import unittest
import pathlib
import importlib
import sys
import os
import io
import contextlib
import subprocess


class TestExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_dir = os.path.abspath(
            os.path.join(__file__, "..", "..", "docs", "examples")
        )

    def test_doc_examples(self):
        for root, _dirs, files in os.walk(self.example_dir):
            try:
                files.remove("main.py")
            except ValueError:
                continue

            module = _import_main_module(root)

            for example in files:
                example_file = os.path.join(root, example)
                argv, stdout_sample = _parse_example_call(example_file)

                with self.subTest(example_dir=root, example=example, argv=argv):
                    exit_status, stdout = _eval_module(module, argv)
                    self.assertEqual(stdout_sample, stdout)
                    self.assertEqual(0, exit_status)


def _parse_example_call(exmaple_file):
    with open(exmaple_file) as fp:
        line = fp.readline()
        argv = line.lstrip("$").split()[1:]
        stdout = fp.read()

    return argv, stdout


def _eval_module(module, argv):
    sys.argv = argv
    exit_status = 0

    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        try:
            module.main()

        except SystemExit as error:
            exit_status = error.code

        stdout = buf.getvalue()

    return exit_status, stdout


def _import_main_module(root):
    path = os.path.join(root, "main.py")
    spec = importlib.util.spec_from_file_location("main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
