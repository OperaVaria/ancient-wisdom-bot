"""
test.py

Unit testing script.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Import Built-in modules.
import sqlite3
import unittest
from pathlib import Path

# Import functions for testing:
from backend.assmbl_func import assemble_posts

# Create an absolute path for the database file.
db_file = Path(__file__).parents[1].resolve() / "db/wisdoms.db"


class Test(unittest.TestCase):
    """Unit tests."""
    def test_tweet_length(self):
        """Test if all tweets are within the length limits (280 char)."""

        # Get number of rows in db.
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM wisdoms")
        row_number = cur.fetchone()[0]
        con.close()

        # Iterate and assert.
        for num in range(row_number):
            print(f"Loop: {num + 1}")
            test_tweet = assemble_posts()
            tweet_length = len(test_tweet)
            self.assertLess(tweet_length, 280, "Too long!")


if __name__ == '__main__':
    unittest.main()
