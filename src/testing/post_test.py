"""
post_test.py

Unittest class that test post creation.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import sqlite3
from contextlib import suppress
from os import remove
from shutil import copyfile
from unittest import TestCase

# Imports from local modules:
from backend.classes import Wisdom, TextPost, ImagePost
from backend.post_func import assemble_posts
from config.path_constants import TEMP_DIR, DB_FILE, GENTIUM_REG_TTF, GENTIUM_BOLD_TTF, TEMP_DB_COPY
from config.settings import IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR


class PostTests(TestCase):
    """Unit tests related to assembling posts."""

    def setUp(self):
        """Copy wisdoms.db file to temp dir.
           Create temp dir if one does not exist."""
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        copyfile(DB_FILE, TEMP_DB_COPY)

    def test_assemble_posts(self):
        """Test if assemble_posts creates valid TextPost and ImagePost objects."""

        # Call assemble function.
        text_post, image_post = assemble_posts(TEMP_DB_COPY, IMG_SIZE, IMG_BG_COLOR,
                                            IMG_TEXT_COLOR, GENTIUM_REG_TTF,
                                            GENTIUM_BOLD_TTF)

        # Assert.
        self.assertIsInstance(text_post, TextPost)
        self.assertIsInstance(image_post, ImagePost)
        self.assertIsNotNone(text_post.full_text)
        self.assertIsNotNone(text_post.accessibility_text)
        self.assertIsNotNone(image_post.image)

    def test_check_char_limits(self):
        """Test if posts meet social media character limits."""

        # Get all Wisdom objects.
        wis_obj_list = []
        con = sqlite3.connect(TEMP_DB_COPY)
        cur = con.cursor()
        for row in cur.execute("SELECT * FROM wisdoms"):
            wis_obj_list.append(Wisdom(*row))
        con.close()

        # Test each TextPost.
        for wis_obj in wis_obj_list:
            text_post = TextPost(wis_obj)
            post_length = len(text_post.full_text)
            comment_length = len(text_post.comment_text)
            with self.subTest("Bluesky check:"):
                self.assertLessEqual(post_length, 300,
                                     f"{wis_obj.id} exceeds Bluesky character limit")
            with self.subTest("Instagram caption check:"):
                self.assertLessEqual(comment_length, 2200,
                                     f"{wis_obj.id} exceeds Instagram caption limit")
            with self.subTest("Mastodon check:"):
                self.assertLessEqual(post_length, 500,
                                     f"{wis_obj.id} exceeds Mastodon character limit")
            with self.subTest("X check:"):
                self.assertLessEqual(post_length, 280,
                                     f"{wis_obj.id} exceeds X character limit")

    def tearDown(self):
        """Remove temporary files if they exist."""
        with suppress(FileNotFoundError):
            remove(TEMP_DB_COPY)


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
