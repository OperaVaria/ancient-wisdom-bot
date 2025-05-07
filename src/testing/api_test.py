"""
api_test.py

Unittest class that tests API functionality.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec, patch

# Imports from external packages:
from atproto_client.exceptions import BadRequestError
from mastodon.errors import MastodonAPIError
from requests import Response
from tweepy.errors import Forbidden

# Imports from local modules:
from backend.classes import TextPost, ImagePost
from backend.multith_func import threaded_login
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

    @patch('backend.multith_func.bluesky_login')
    @patch('backend.multith_func.insta_login')
    @patch('backend.multith_func.mastodon_login')
    @patch('backend.multith_func.x_auth')
    def test_threaded_login(self, mock_x_auth, mock_mastodon_login,
                        mock_insta_login, mock_bluesky_login):
        """Test concurrent login functionality."""

        # Mock constants that are used in the function.
        with patch('backend.multith_func.INSTA_SESSION', 'mock_session'), \
            patch('backend.multith_func.INSTA_DELAY_RANGE', 'mock_delay'):

            # Setup mock returns.
            mock_bluesky_login.return_value = "bs_client"
            mock_insta_login.return_value = "insta_client"
            mock_mastodon_login.return_value = "mastodon_api"
            mock_x_auth.return_value = ("x_api", "x_client")

            # Test login data.
            keys = {
                "bluesky": {"handle": "test", "password": "test"},
                "instagram": {"username": "test", "password": "test"},
                "mastodon": {"access_token": "test", "api_base_uri": "test"},
                "x": {"key": "value"}
            }

            # Call threaded_login function.
            result = threaded_login(keys)

            # Assert.
            self.assertEqual(result, ("bs_client", "insta_client", "mastodon_api",
                                      "x_api", "x_client"))
            mock_bluesky_login.assert_called_once_with(
                keys["bluesky"]["handle"],
                keys["bluesky"]["password"]
            )
            mock_insta_login.assert_called_once_with(
                keys["instagram"]["username"],
                keys["instagram"]["password"],
                'mock_session',
                'mock_delay'
            )
            mock_mastodon_login.assert_called_once_with(
                keys["mastodon"]["access_token"],
                keys["mastodon"]["api_base_uri"]
            )
            mock_x_auth.assert_called_once_with(keys["x"])


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
