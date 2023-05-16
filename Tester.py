import importlib
import unittest


def main():
    modules = ["Tests.Login_system_tests", "Tests.Queries_tests"]
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for module in modules:
        test_module = importlib.import_module(module)
        test_suite.addTests(loader.loadTestsFromModule(test_module))
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == "__main__":
    main()
