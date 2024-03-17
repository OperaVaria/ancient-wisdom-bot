"""
db_func.py

Functions related to database operations.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports:
import sqlite3
from pathlib import Path
from .wisdom_class import Wisdom

# Create an absolute path for the database file.
db_file = Path(__file__).parents[1].resolve() / "db/wisdoms.db"


def db_get():
    """Get attributes from database. Create Wisdom instance."""
    # Database access.
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    # Call select random function.
    wis_tuple = select_random(cur)
    # If result is None (no more unused quotes left).
    if wis_tuple == None:
        # Reset "used" values.
        cur.execute("UPDATE wisdoms SET used = 0 WHERE used = 1")
        con.commit()
        # Print notification.
        print("\nNo more items, database reset!\n")
        # Fetch again.        
        wis_tuple = select_random(cur) 
    # Create Wisdom object.
    wis_obj = Wisdom(*wis_tuple)    
    # Change "used" value to true/1.
    id_tuple = (wis_obj.id,)
    cur.execute("UPDATE wisdoms SET used = 1 WHERE id_title = ?", id_tuple)
    con.commit()
    # Close connection.
    con.close()
    return wis_obj

def select_random(cur):
    """Select a random row from the database."""
    # SQLite "SELECT RANDOM" command.
    com_random = "SELECT * FROM wisdoms WHERE used = 0 ORDER BY RANDOM()"
    # Fetch row.    
    res = cur.execute(com_random)
    wis_tuple = res.fetchone()
    return wis_tuple


# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
