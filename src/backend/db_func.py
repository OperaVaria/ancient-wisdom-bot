"""
db_func.py

Functions related to database operations.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports:
import sqlite3
from pathlib import Path
from backend.classes import Wisdom

# Create an absolute path for the db file.
db_file = Path(__file__).parents[2].resolve() / "db/wisdoms.db"


def db_get():
    """Get attributes from database. Create Wisdom instance."""
    # Database access.
    con = sqlite3.connect(db_file)
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
    # Call print remaining function.
    print_remaining(cur)
    # Close connection.
    con.close()
    return wis_obj


def select_random(cur):
    """Select a random row from the database."""
    # SQLite "SELECT RANDOM()" command.
    com_random = "SELECT * FROM wisdoms WHERE used = 0 ORDER BY RANDOM()"
    # Fetch row.
    res = cur.execute(com_random)
    wis_tuple = res.fetchone()
    return wis_tuple


def db_reset(con, cur):
    """Function to reset all 'used' values to False(0)."""
    # Reset "used" values.
    cur.execute("UPDATE wisdoms SET used = 0 WHERE used = 1")
    con.commit()
    # Print notification.
    print("\nNo more items, database reset!\n")


def print_remaining(cur):
    """Print out number of remaining unused quotes."""
    cur.execute("SELECT COUNT(*) FROM wisdoms WHERE used = 0")
    rem_quotes = cur.fetchone()[0]
    print(f"{rem_quotes} items remaining in the database.")
    return rem_quotes


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
