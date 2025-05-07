"""
api_test.py

Unittest class that tests API functionality.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec

# Imports from external packages:
from atproto_client.exceptions import BadRequestError
from mastodon.errors import MastodonAPIError
from requests import Response
from tweepy.errors import Forbidden

# Imports from local modules:
from backend.classes import TextPost, ImagePost
from backend.post_func import bluesky_post, mastodon_post, x_post


class APITests(TestCase):
    """Unit tests related to API processes."""

    def setUp(self):
        """Create mock objects for API testing."""

        # Client
        self.mock_client = MagicMock()

        # TextPost
        self.mock_text_post = MagicMock(spec=TextPost)
        self.mock_text_post.full_text = "Test text."
        self.mock_text_post.comment_text = "Test comment."
        self.mock_text_post.accessibility_text = "Test alt text."

        # ImagePost
        self.mock_image_post = MagicMock(spec=ImagePost)
        self.mock_image_post.open_bin.return_value = b"fake_image_data"
        self.mock_image_post.path = create_autospec(Path)

        # Response
        self.mock_response_failed = MagicMock(spec=Response)
        self.mock_response_failed.ok = False
        self.mock_response_failed.status_code = 400
        self.mock_response_failed.reason = "Post too long!"


    def test_bluesky_post_fallback(self):
        """Test Bluesky image post fallback mechanism when text post fails."""

        # Make text post fail, image post succeed.
        self.mock_client.send_post.side_effect = BadRequestError(self.mock_response_failed)
        self.mock_client.send_image.return_value = {"ok": True}

        # Test the function.
        result = bluesky_post(self.mock_client, self.mock_image_post, self.mock_text_post)

        # Assert.
        self.mock_client.send_post.assert_called_once_with(text=self.mock_text_post.full_text)
        self.mock_client.send_image.assert_called_once()
        self.mock_image_post.open_bin.assert_called_once()
        self.assertEqual(result, {"ok": True})

    def test_mastodon_post_fallback(self):
        """Test Mastodon image post fallback mechanism when text post fails."""

        # Make text post fail, image post succeed.
        self.mock_client.status_post.side_effect = [MastodonAPIError(self.mock_response_failed),
                                                    {"ok": True}]
        self.mock_client.media_post.return_value = {"id": 1}

        # Test the function.
        result = mastodon_post(self.mock_client, self.mock_image_post, self.mock_text_post)

        # Assert.
        self.assertEqual(self.mock_client.status_post.call_count, 2)
        self.mock_client.media_post.assert_called_once()
        self.assertEqual(result, {"ok": True})

    def test_x_post_fallback(self):
        """Test X image post fallback mechanism when text post fails."""

        # Make text post fail, image post succeed.
        self.mock_client.create_tweet.side_effect = [Forbidden(self.mock_response_failed),
                                                     {"ok": True}]
        self.mock_client.media_upload.media_id = 1

        # Test the function.
        result = x_post(self.mock_client, self.mock_client,
                        self.mock_image_post, self.mock_text_post)

        # Assert.
        self.assertEqual(self.mock_client.create_tweet.call_count, 2)
        self.mock_client.media_upload.assert_called_once()
        self.assertEqual(result, {"ok": True})


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
