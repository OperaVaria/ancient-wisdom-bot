"""
auth_func.py

Functions for social media API authentication and login.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging
from os.path import exists as os_exists

# Imports from external packages:
from atproto import Client as BsClient
from atproto_client.exceptions import UnauthorizedError
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientUnauthorizedError, LoginRequired
from mastodon import Mastodon
from mastodon.errors import MastodonUnauthorizedError
from tweepy import API as XAPI
from tweepy import Client as XClient
from tweepy import OAuth1UserHandler
from tweepy.errors import Unauthorized

# Setup logging:
logger = logging.getLogger(__name__)


def bluesky_login(login, password):
    """
    Set up Bluesky login with error handling.

    Args:
        login: Bluesky handle.
        password: Bluesky password.

    Returns:
        bs_cl: authenticated Bluesky Client object.

    Raises:
        UnauthorizedError: if login fails.
    """
    bs_cl = BsClient()
    try:
        bs_cl.login(login, password)
        return bs_cl
    except UnauthorizedError as e:
        logger.error("Bluesky login failed: %s", e)
        raise


def insta_login(username, password, settings_path, delay_range):
    """
    Set up Instagram login using either username and password,
    or previously saved session data.

    Args:
        username: Instagram username.
        password: Instagram password.
        settings_path: Path to session settings.
        delay_range(list[int]):
            interpreted as a range between two numbers.
            A random delay in seconds between
            requests to mimic live user interaction.

    Returns:
        in_cl: authenticated Instagram Client object.

    Raises:
        ClientUnauthorizedError: if login fails with both methods.
    """
    # Create Client instance.
    in_cl = InstaClient()
    # Add random delay.
    in_cl.delay_range = delay_range
    # Try login using saved session.
    if _try_session_login(in_cl, username, password, settings_path):
        return in_cl
    # Try login via username and password.
    if _try_credentials_login(in_cl, username, password, settings_path):
        return in_cl
    # If both login methods fail, raise error.
    raise ClientUnauthorizedError(
        "Login failed: couldn't login user with either password or session"
    )


def _try_session_login(client, username, password, settings_path):
    """
    Helper function for insta_login, attempts login via saved session.

    Args: see above.

    Returns:
        Login success boolean.
    """
    # If settings file does not exist: early return False.
    if not os_exists(settings_path):
        return False
    # Attempt login with error handling.
    try:
        session = client.load_settings(settings_path)
        client.set_settings(session)
        client.login(username, password)
        # Verify if session is valid. If not, log error, return false.
        try:
            client.get_timeline_feed()
            return True
        except LoginRequired:
            logger.error("Session is invalid, need to login via username and password")
            # Preserve device UUIDs across logins.
            old_session = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            return False
    except ClientUnauthorizedError as e:
        logger.error("Couldn't login user using session information: %s", e)
        return False


def _try_credentials_login(client, username, password, settings_path):
    """
    Helper function for insta_login, attempts login via username and password.

    Args: see above.

    Returns:
        Login success boolean.
    """
    try:
        if client.login(username, password):
            # if successful: dump session settings.
            client.dump_settings(settings_path)
            return True
        return False
    except ClientUnauthorizedError as e:
        logger.error("Couldn't login user using username and password: %s", e)
        return False


def mastodon_login(access_token, api_base_uri):
    """
    Set up Mastodon login with error handling.

    Args:
        access_token: Mastodon application access token.
        api_base_uri: Mastodon application redirect URI.

    Returns:
        mt_api: authenticated Mastodon API object.

    Raises:
        MastodonUnauthorizedError: if authentication fails.
    """
    try:
        mt_api = Mastodon(access_token=access_token, api_base_url=api_base_uri)
        return mt_api
    except MastodonUnauthorizedError as e:
        logger.error("Mastodon authentication failed: %s", e)
        raise


def x_auth(x_keys):
    """
    Authenticate both versions of the X API.

    Args:
        x_keys: dictionary containing all required keys and tokens.

    Returns:
        x_api: authenticated v1.1 X API object.
        x_cl: authenticated v2 X Client object.

    Raises:
        Unauthorized: If either authentication fails.
    """
    # X API v1.1 authentication with error handling.
    try:
        x_oauth1 = OAuth1UserHandler(
            access_token_secret=x_keys["access_token_secret"],
            access_token=x_keys["access_token"],
            consumer_key=x_keys["consumer_key"],
            consumer_secret=x_keys["consumer_secret"],
        )
        x_api = XAPI(x_oauth1)
    except Unauthorized as e:
        logger.error("X API v1.1 authentication failed: %s", e)
        raise
    # X API v2 authentication with error handling.
    try:
        x_cl = XClient(
            access_token_secret=x_keys["access_token_secret"],
            access_token=x_keys["access_token"],
            bearer_token=x_keys["bearer_token"],
            consumer_key=x_keys["consumer_key"],
            consumer_secret=x_keys["consumer_secret"],
            wait_on_rate_limit=True,
        )
    except Unauthorized as e:
        logger.error("X API v2 authentication failed: %s", e)
        raise
    return x_api, x_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
