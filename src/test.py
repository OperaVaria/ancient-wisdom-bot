"""
test.py

Unit testing script with a TUI.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Import built-in modules.
import unittest

# Imports from external packages:
from pick import pick

# Imports from local modules:
import testing.db_test as db_tests
import testing.class_test as class_tests
from testing.shared import copy_db, del_temp_db, error_crash

def run_db_tests():
    """Steps needed to run database test suite."""

    # Copy database to temporary location.
    copy_db()

    # Print separator.
    print("\n----------------------------------------------------------------------\n")

    # Load and run tests.
    test_suite = unittest.TestLoader().loadTestsFromModule(db_tests)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Temp file cleanup.
    del_temp_db()

    # return prompt.
    input("\nPress Enter to return...")

def run_class_tests():
    """Steps needed to run class test suite."""

    # Print separator.
    print("\n----------------------------------------------------------------------\n")

    # Load and run tests.
    test_suite = unittest.TestLoader().loadTestsFromModule(class_tests)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    # return prompt.
    input("\nPress Enter to return...")


def test_menu():
    """Test routine select menu."""

    # Menu variables.
    title = "Ancient Wisdom Bot 2.1.0 Unittest\n\nSelect functionality to test:"
    options = ["1. Database operations", "2. Class instantiation", "3. Exit"]

    # Menu loop.
    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:  # DB
                run_db_tests()
            case 1:  # Classes
                run_class_tests()
            case 2: # Exit (break loop).
                break
            case _:  # Incorrect selection (should not happen).
                error_crash("Selection error!")


# Launch test menu.
if __name__ == "__main__":
    test_menu()
