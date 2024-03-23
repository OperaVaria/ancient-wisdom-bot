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
from backend.classes import Wisdom

# Create an absolute path for the database file.
db_file = Path(__file__).parents[1].resolve() / "db/wisdoms.db"


class Test(unittest.TestCase):
    """Unit tests."""

    def test_tweet_length(self):
        """Test if all text posts are within Twitter length limits (280 char)."""

        # Create list of all db items.
        wis_obj_list = []
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        for row in cur.execute("SELECT * FROM wisdoms"):
            wis_obj_list.append(Wisdom(*row))
        con.close()

        # Iterate and assert.
        for i in wis_obj_list:
            text_post = i.create_text_post()
            post_length = len(text_post)
            print(f"{i.id}: {post_length}")
            self.assertLess(post_length, 280, f"{i.id} is too long!")


if __name__ == "__main__":
    unittest.main()
