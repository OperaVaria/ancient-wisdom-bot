"""
db_func.py

Functions related to database operations.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging
import sqlite3
from pathlib import Path

# Import Wisdom class.
from backend.classes import Wisdom

# Setup logging.
logger = logging.getLogger(__name__)

# Create an absolute path for the db file.
DB_FILE_PATH = Path(__file__).parents[2].resolve() / "db/wisdoms.db"


def db_get():
    """
    Get attributes from database and create a Wisdom instance.

    Returns:
        Wisdom: An instance of the Wisdom class with data from the database.

    Raises:
        sqlite3.Error: If there's a database-related error.
    """
    try:
        # Database access.
        con = sqlite3.connect(DB_FILE_PATH)
        cur = con.cursor()
        # Call select random function.
        wis_tuple = select_random(cur)
        # If result is None ( = no more unused quotes left).
        if wis_tuple is None:
            # Call database reset function.
            db_reset(con, cur)
            # Fetch random again.
            wis_tuple = select_random(cur)
        # Create Wisdom object.
        wis_obj = Wisdom(*wis_tuple)
        # Change "used" value to True(1).
        id_tuple = (wis_obj.id,)
        cur.execute("UPDATE wisdoms SET used = 1 WHERE id_title = ?", id_tuple)
        con.commit()
        # Call log remaining function.
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
        wis_tuple/None: A tuple with the row data or None if no rows found.
    """
    # SQLite "SELECT RANDOM()" command.
    com_random = "SELECT * FROM wisdoms WHERE used = 0 ORDER BY RANDOM()"
    # Fetch row.
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
    # Reset "used" values.
    cur.execute("UPDATE wisdoms SET used = 0 WHERE used = 1")
    con.commit()
    # Log notification.
    logger.info("\nNo more items, database reset!\n")


def log_remaining(cur):
    """
    Log and return the number of remaining unused quotes.

    Args:
        cur: SQLite cursor object.

    Returns:
        int: Number of remaining unused quotes.
    """
    cur.execute("SELECT COUNT(*) FROM wisdoms WHERE used = 0")
    rem_quotes = cur.fetchone()[0]
    logger.info("%d items remaining in the database.", rem_quotes)
    return rem_quotes


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
