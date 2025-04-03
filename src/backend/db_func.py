"""
db_func.py

Functions related to database operations.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging
import sqlite3

# Import Wisdom dataclass.
from backend.classes import Wisdom

# Setup logging.
logger = logging.getLogger(__name__)


def db_get(db_file):
    """
    Get attributes from database and create a Wisdom instance.

    Args:
        db_file: Path to database file.

    Returns:
        wis_obj: instance of the Wisdom dataclass populated from the database.

    Raises:
        sqlite3.Error: if there is a database-related error.
    """
    try:
        # Database access.
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        # Call select random function.
        wis_tuple = select_random(cur)
        # If result is None ( = no more unused quotes left):
        # call reset database function, fetch random again.
        if wis_tuple is None:
            db_reset(con, cur)
            wis_tuple = select_random(cur)
        # Create Wisdom object.
        wis_obj = Wisdom(*wis_tuple)
        # Change "used" value to True(1).
        id_tuple = (wis_obj.id,)
        cur.execute("UPDATE wisdoms SET used = 1 WHERE id_title = ?", id_tuple)
        con.commit()
        # Call log_remaining function.
        log_remaining(cur)
        # Close connection.
        con.close()
        return wis_obj
    except sqlite3.Error as e:
        logger.error("Database error occurred: %s", e)
        raise


def select_random(cur):
    """
    Select a random row from the database.

    Args:
        cur: SQLite cursor object.

    Returns:
        wis_tuple/None: a tuple with the row data or None if no rows found.
    """
    com_random = "SELECT * FROM wisdoms WHERE used = 0 ORDER BY RANDOM()"
    res = cur.execute(com_random)
    wis_tuple = res.fetchone()
    return wis_tuple


def db_reset(con, cur):
    """
    Reset all 'used' values to False(0).

    Args:
        con: SQLite connection object.
        cur: SQLite cursor object.
    """
    cur.execute("UPDATE wisdoms SET used = 0 WHERE used = 1")
    con.commit()
    logger.info("No more items, database reset")


def log_remaining(cur):
    """
    Log and return the number of remaining unused quotes.

    Args:
        cur: SQLite cursor object.

    Returns:
        rem_quotes(int): number of remaining unused quotes.
    """
    cur.execute("SELECT COUNT(*) FROM wisdoms WHERE used = 0")
    rem_quotes = cur.fetchone()[0]
    logger.info("%d items remaining in the database", rem_quotes)
    return rem_quotes


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
