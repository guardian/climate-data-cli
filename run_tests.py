#!/usr/bin/env python
import unittest

def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")

    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)
