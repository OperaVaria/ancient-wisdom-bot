"""
test.py

Unit testing script with a Pick TUI.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from logging import critical as logging_critical
from sys import exit as sys_exit
from unittest import TestLoader, TextTestRunner

# Imports from external packages:
from pick import pick

# Imports from local modules:
import testing.api_test as api_tests
import testing.db_test as db_tests
import testing.class_test as class_tests
import testing.post_test as post_tests
import testing.workflow_test as workflow_tests


def run_tests(module):
    """
    Steps needed to run test suite.

    Args:
        module: imported module to load tests from.
    """

    # Print separator.
    print("\n----------------------------------------------------------------------\n")

    # Load and run tests.
    test_suite = TestLoader().loadTestsFromModule(module)
    TextTestRunner(verbosity=2).run(test_suite)

    # Return prompt.
    input("\nPress Enter to return...")


def test_menu():
    """Test routine select menu using the Pick TUI module."""

    # Menu variables.
    title = "Ancient Wisdom Bot 2.1.0 Unittest\n\nSelect functionality to test:"
    options = ["1. Database operations", "2. Class instantiation", "3. Assembling posts",
               "4. API requests", "5. Workflow integration", "6. Exit"]

    # Menu loop.
    while True:
        _, index = pick(options, title, indicator="=>", default_index=0)
        match index:
            case 0:  # DB
                run_tests(db_tests)
            case 1:  # Classes
                run_tests(class_tests)
            case 2: # Posts
                run_tests(post_tests)
            case 3: # API
                run_tests(api_tests)
            case 4: # Workflow
                run_tests(workflow_tests)
            case 5: # Exit (break loop)
                break
            case _:  # Incorrect selection (should not happen).
                # Logs critical error. Exits with error code: 1.
                logging_critical("Selection error!")
                sys_exit(1)


# Launch test menu.
if __name__ == "__main__":
    test_menu()
