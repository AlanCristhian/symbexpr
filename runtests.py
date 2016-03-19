"""Execute linters and tests."""

import multiprocessing
import pathlib
import subprocess
import sys
import time
import unittest
import argparse
import importlib


MODULES = [str(p) for p in pathlib.Path('.').glob('**/*.py')]


def run_linter_once(args):
    """Run a linter program from the command line."""
    process = subprocess.Popen(args, start_new_session=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, _ = process.communicate()
    if output:
        print(output.decode())
    return output


def run_linter_many(linter, *args):
    """Run the linter one time for module in MODULES constant."""
    for module in MODULES:
        arguments = [sys.executable, "-m", linter, module, *args]
        have_output = run_linter_once(arguments)
        if have_output:
            return True
    return False


def catch_linter_errors(linter, args, accept_many_modules=True):
    """Run a linter and show their errors."""
    print(linter)
    if accept_many_modules:
        arguments = [sys.executable, "-m", linter, *args]
        have_output = run_linter_once(arguments)
        if have_output:
            return True
    else:
        have_output = run_linter_many(linter, *args)
        if have_output:
            return True
    return False


class Main:
    """Set up and run test, servers, and linters."""
    def __init__(self, argument):
        self.process = None
        self.argument = argument
        pylint_arguments = ["--rcfile=pylint.ini", "-d I",
                            "-j %d" % multiprocessing.cpu_count(), *MODULES]
        if self.argument.linters:
            start = time.perf_counter()
            # pylint: disable=too-many-boolean-expressions
            if catch_linter_errors("pyflakes", MODULES) \
            or catch_linter_errors("pylint", pylint_arguments) \
            or catch_linter_errors("mccabe", ["--min", "5"],
                                   accept_many_modules=False) \
            or catch_linter_errors("bandit", ()) \
            or catch_linter_errors("pep8", (), accept_many_modules=False) \
            or catch_linter_errors("pydocstyle", (),
                                   accept_many_modules=False):  # nopep8
                return
            end = time.perf_counter() - start
            print("\nRan 6 linter in %.3fs\n%s\nOK" % (end, "-"*70))
        else:
            self.load_and_run_tests()

    def load_tests(self):
        """Load rithg test with argument."""
        files = pathlib.Path(".").glob("*.py")
        paths = (p.parent / p.stem for p in files)
        modules = (str(p).replace("/", ".") for p in paths)
        test_modules = (m for m in modules if "__" not in m if "test" in m)
        if self.argument.module is not None:
            valid_modules = (self.argument.module,)
        else:
            valid_modules = test_modules
        return (importlib.import_module(m) for m in valid_modules)

    def load_and_run_tests(self):
        """Run all tests."""
        valid_modules = self.load_tests()
        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner(failfast=self.argument.failfast)
        suite = unittest.TestSuite()
        for module in valid_modules:
            suite.addTest(loader.loadTestsFromModule(module))
        runner.run(suite)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-l", "--linters", action="store_true",
                        help="Run all linters")
    PARSER.add_argument("-m", "--module",
                        help="Run specific test module")
    PARSER.add_argument("-f", "--failfast", action="store_true",
                        help="Stop the test run on the first error or failure")
    ARGUMENT = PARSER.parse_args()
    Main(ARGUMENT)
