import unittest
import os
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

            script = os.path.join(root, "main.py")

            for example in files:
                example_file = os.path.join(root, example)
                argv, stdout_sample = _parse_example_call(example_file)

                with self.subTest(example_dir=root, example=example, argv=argv):
                    exit_status, stdout = _eval_script(script, argv)
                    self.assertEqual(stdout_sample, stdout)
                    self.assertEqual(0, exit_status)


def _parse_example_call(exmaple_file):
    with open(exmaple_file) as fp:
        line = fp.readline()
        argv = line.lstrip("$").split()[2:]
        stdout = fp.read()

    return argv, stdout


def _eval_script(script, argv):
    result = subprocess.run([".venv/bin/python", script] + argv, capture_output=True)

    output = result.stdout.decode()

    if result.stderr:
        output += "STDERR:\n" + result.stderr.decode()

    return result.returncode, output
