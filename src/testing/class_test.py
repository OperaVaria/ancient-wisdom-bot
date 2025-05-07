"""
class_test.py

Unittest class that tests project classes.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from os import path, remove
from unittest import TestCase

# Imports from local modules:
from backend.classes import Wisdom, ImagePost, TextPost
from config.path_constants import GENTIUM_REG_TTF, GENTIUM_BOLD_TTF, TEMP_DIR
from config.settings import IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR


class ClassTests(TestCase):
    """Tests class implementations."""

    def setUp(self):
        """Set up dummy tuple with test data."""
        self.test_data = ("test_id", "original text", "translation text",
            "Author", "Locus 1.1", "𝑳𝒐𝒄𝒖𝒔 1.1", "This is a comment", False)

    def test_wisdom_object_creation(self):
        """Test Wisdom class instantiation with proper attributes."""

        # Create instance.
        wisdom = Wisdom(*self.test_data)

        # Assert.
        self.assertEqual(wisdom.id, "test_id")
        self.assertEqual(wisdom.original, "original text")
        self.assertEqual(wisdom.translation, "translation text")
        self.assertEqual(wisdom.attribution, "Author")
        self.assertEqual(wisdom.locus, "Locus 1.1")
        self.assertEqual(wisdom.locus_formatted, "𝑳𝒐𝒄𝒖𝒔 1.1")
        self.assertEqual(wisdom.comment, "This is a comment")
        self.assertEqual(wisdom.used, False)

    def test_text_post_creation(self):
        """Test TextPost class instantiation and content formatting."""

        # Create instances.
        wisdom = Wisdom(*self.test_data)
        text_post = TextPost(wisdom)

        # Assert.
        self.assertIn("original text", text_post.full_text)
        self.assertIn("translation text", text_post.full_text)
        self.assertIn("Author", text_post.full_text)
        self.assertIn("𝑳𝒐𝒄𝒖𝒔 1.1", text_post.full_text)
        self.assertIn("This is a comment", text_post.full_text)
        self.assertEqual('Original quote: "original text"\n'
                         'Translation: "translation text"\n'
                         'Source: "Author in 𝑳𝒐𝒄𝒖𝒔 1.1"',
                         text_post.accessibility_text)
        self.assertEqual(text_post.comment_text, "This is a comment")

    def test_image_post_creation(self):
        """Test ImagePost class and image generation."""

        # Create instances.
        wisdom = Wisdom(*self.test_data)
        image_post = ImagePost(wisdom, IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR,
                            GENTIUM_REG_TTF, GENTIUM_BOLD_TTF)

        # Test if image was created.
        self.assertIsNotNone(image_post.image)
        self.assertEqual(image_post.image.size, IMG_SIZE)

        # Test save_image method.
        test_path = path.join(TEMP_DIR, "test_image.jpg")
        image_post.save_image(test_path)
        self.assertTrue(path.exists(test_path))

        # Test open_bin method.
        bin_data = image_post.open_bin()
        self.assertIsInstance(bin_data, bytes)

        # Clean up.
        if path.exists(test_path):
            remove(test_path)

    def test_image_post_font_fallback(self):
        """Test ImagePost font fallback mechanism when fonts are not available."""

        # Create instance.
        wisdom = Wisdom(*self.test_data)

        # Use non-existent font paths.
        image_post = ImagePost(wisdom, IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR,
                            "nonexistent_font.ttf", "nonexistent_font_bold.ttf")

        # Test if image was created despite font issues.
        self.assertIsNotNone(image_post.image)
        self.assertEqual(image_post.image.size, IMG_SIZE)

    def test_image_post_path_error(self):
        """Test error handling when trying to open binary before saving image."""

        # Create instance.
        wisdom = Wisdom(*self.test_data)
        image_post = ImagePost(wisdom, IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR,
                            GENTIUM_REG_TTF, GENTIUM_BOLD_TTF)

        # Attempt to open binary before saving.
        with self.assertRaises(TypeError):
            image_post.open_bin()


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
