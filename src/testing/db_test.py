"""
db_test.py

Unittest class that tests database functionality.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import sqlite3
from contextlib import suppress
from os import remove
from shutil import copyfile
from unittest import TestCase

# Imports from local modules:
from backend.db_func import db_get, db_reset, log_remaining
from backend.classes import Wisdom
from config.path_constants import DB_FILE, TEMP_DIR, TEMP_DB_COPY, FAKE_DB_FILE


class DatabaseTests(TestCase):
    """Database related unit tests."""

    def setUp(self):
        """Copy wisdoms.db file to temp dir.
           Create temp dir if one does not exist."""
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        copyfile(DB_FILE, TEMP_DB_COPY)

    def test_db_get_error_handling(self):
        """Test db_get with invalid database path."""
        with self.assertRaises(sqlite3.Error):
            db_get(FAKE_DB_FILE)

    def test_db_get_returns_wisdom_object(self):
        """Test if db_get returns a valid Wisdom object."""

        # Call db_get on temporary copy of the db file.
        wisdom = db_get(TEMP_DB_COPY)

        # Assert.
        self.assertIsInstance(wisdom, Wisdom)
        self.assertIsNotNone(wisdom.id)
        self.assertIsNotNone(wisdom.original)
        self.assertIsNotNone(wisdom.translation)
        self.assertIsNotNone(wisdom.attribution)
        self.assertIsNotNone(wisdom.locus)
        self.assertIsNotNone(wisdom.locus_formatted)
        self.assertIsNotNone(wisdom.comment)
        self.assertIsNotNone(wisdom.used)

    def test_db_reset_clears_used_flags(self):
        """Test if db_reset properly resets used flags."""

        # Set up connection.
        con = sqlite3.connect(TEMP_DB_COPY)
        cur = con.cursor()

        # Set all items to used.
        cur.execute("UPDATE wisdoms SET used = 1")
        con.commit()

        # Call db_reset function.
        db_reset(con, cur)

        # Check the result.
        cur.execute("SELECT COUNT(*) FROM wisdoms WHERE used = 0")
        flagged_used = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM wisdoms")
        total = cur.fetchone()[0]

        # Close and assert.
        con.close()
        self.assertEqual(flagged_used, total, "Not all rows were reset.")

    def test_log_remaining_counts_correctly(self):
        """Test if log_remaining correctly counts unused items."""

        # Set up connection.
        con = sqlite3.connect(TEMP_DB_COPY)
        cur = con.cursor()

        # Set a known state.
        cur.execute("UPDATE wisdoms SET used = 0")
        cur.execute("UPDATE wisdoms SET used = 1 WHERE id_title LIKE 'test%'")
        con.commit()

        # Get the correct count.
        cur.execute("SELECT COUNT(*) FROM wisdoms WHERE used = 0")
        expected = cur.fetchone()[0]

        # Test the function.
        result = log_remaining(cur)

        # Close and assert.
        con.close()
        self.assertEqual(result, expected, "Incorrect count of remaining items.")

    def tearDown(self):
        """Remove temporary files if they exist."""
        with suppress(FileNotFoundError):
            remove(TEMP_DB_COPY)
            remove(FAKE_DB_FILE)


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
