"""
post_test.py

Unittest class that tests the workflow integration.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from os import path, remove
from unittest import TestCase
from unittest.mock import MagicMock, patch

# Imports from local modules:
from backend.classes import Wisdom, TextPost, ImagePost
from backend.multith_func import threaded_posting
from config.path_constants import GENTIUM_REG_TTF, GENTIUM_BOLD_TTF, TEMP_POST_IMG
from config.settings import IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR


class IntegrationTests(TestCase):
    """Unit tests related to the posting workflow."""

    def test_post_workflow_integration(self):
        """Integration test for the full posting workflow."""        

        # Create mock API clients.
        mock_bs_cl = MagicMock()
        mock_in_cl = MagicMock()
        mock_mt_api = MagicMock()
        mock_x_api = MagicMock()
        mock_x_cl = MagicMock()

        # Set up return values for the mock clients.
        mock_bs_cl.send_post.return_value = {"id": "123"}
        mock_in_cl.photo_upload.return_value = {"id": "456"}
        mock_mt_api.status_post.return_value = {"id": "789"}
        mock_x_cl.create_tweet.return_value = {"id": "012"}

        # Patch dependencies.
        with patch('backend.post_func.assemble_posts') as mock_assemble:

            # Create real objects for mock assemble function.
            test_data = ("test_id", "original text", "translation text",
                         "Author", "Locus 1.1", "𝑳𝒐𝒄𝒖𝒔 1.1", "This is a comment", False)
            wisdom = Wisdom(*test_data)
            text_post = TextPost(wisdom)
            image_post = ImagePost(wisdom, IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR,
                                GENTIUM_REG_TTF, GENTIUM_BOLD_TTF)

            # Save image to temp path.
            image_post.save_image(TEMP_POST_IMG)

            # Mock the assemble_posts function to return the objects.
            mock_assemble.return_value = (text_post, image_post)

            # Call threaded_posting function.
            results = threaded_posting(
                mock_bs_cl, mock_in_cl, mock_mt_api, mock_x_api, mock_x_cl,
                text_post, image_post
            )

            # Verify all platforms were posted to.
            mock_bs_cl.send_post.assert_called_once()
            mock_in_cl.photo_upload.assert_called_once()
            mock_mt_api.status_post.assert_called_once()
            mock_x_cl.create_tweet.assert_called_once()

            # Verify response objects.
            self.assertEqual(len(results), 4)

            # Clean up.
            if path.exists(TEMP_POST_IMG):
                remove(TEMP_POST_IMG)


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
