"""
shared.py

Functions shared between multiple test routines.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Import built-in modules:
import logging
from shutil import copyfile as shutil_copyfile
from sys import exit as sys_exit
from os import remove as os_remove

# Imports from local modules:
from config.path_constants import DB_FILE, TEMP_DIR, TEMP_DB_COPY


def copy_db():
    "Copy db to temporary location."
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    shutil_copyfile(DB_FILE, TEMP_DB_COPY)


def del_temp_db():
    "Remove temporary database file."
    os_remove(TEMP_DB_COPY)


def error_crash(message):
    """Function to handle serious errors.
    Logs critical error message and exits program.
    Exit status 1."""
    logging.critical(message)
    sys_exit(1)


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
