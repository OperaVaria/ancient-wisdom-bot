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
from atproto_core.exceptions import AtProtocolError
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, LoginRequired
from threadspy import ThreadsAPI
from tweepy import API as XAPI
from tweepy import Client as XClient
from tweepy import OAuth1UserHandler
from tweepy.errors import TweepyException

# Setup logging:
logger = logging.getLogger(__name__)


def bluesky_login(login, password):
    """
    Set up Bluesky login with error handling.

    Args:
        login: Bluesky handle.
        password: Bluesky password.

    Returns:
        BsClient: Authenticated Bluesky client object.

    Raises:
        Exception: If login fails.
    """
    bs_cl = BsClient()
    try:
        bs_cl.login(login, password)
        return bs_cl
    except AtProtocolError as e:
        logger.error("Bluesky login failed: %s", e)
        raise


def insta_login(username, password, settings_path, delay_range):
    """
    Set up Instagram login using either username and password
    or previously saved session data.

    Args:
        username: Instagram username.
        password: Instagram password.
        settings_path: Path to session settings.
        delay_range: list[int] range between two numbers,
                     random delay in seconds between
                     requests to mimic live user interaction.

    Returns:
        in_cl: Authenticated Instagram client object.

    Raises:
        ClientError: If login fails with both methods.
    """
    # Create Client instance.
    in_cl = InstaClient()
    # Add random delay to mimic live user interactions.
    in_cl.delay_range = delay_range
    # Try login using saved session.
    if _try_session_login(in_cl, username, password, settings_path):
        return in_cl
    # Try login via username and password.
    if _try_credentials_login(in_cl, username, password, settings_path):
        return in_cl
    # If both login methods fail, raise error.
    raise ClientError(
        "Login failed: couldn't login user with either password or session"
    )


def _try_session_login(client, username, password, settings_path):
    """Helper function for insta_login to attempt login via saved session."""
    # If settings file does not exist: early return False.
    if not os_exists(settings_path):
        return False
    # Attempt login with error handling.
    try:
        session = client.load_settings(settings_path)
        client.set_settings(session)
        client.login(username, password)
        # Verify if session is valid.
        try:
            client.get_timeline_feed()
            return True
        # If not, raise exception.
        except LoginRequired:
            logger.error("Session is invalid, need to login via username and password")
            # Preserve device UUIDs across logins
            old_session = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            return False
    except ClientError as e:
        logger.error("Couldn't login user using session information: %s", e)
        return False


def _try_credentials_login(client, username, password, settings_path):
    """Helper function for insta_login to attempt login via username and password."""
    try:
        logger.info(
            "Attempting to login via username and password. Username: %s", username
        )
        if client.login(username, password):
            logger.info(
                "Successfully logged in to Instagram as %s using credentials", username
            )
            client.dump_settings(settings_path)
            return True
        return False
    except ClientError as e:
        logger.error("Couldn't login user using username and password: %s", e)
        return False


def threads_login(username, password):
    """
    Set up Threads login with error handling.

    Args:
        username: Threads username.
        password: Threads password.

    Returns:
        ThreadsAPI: Authenticated Threads API object.
    
    Raises:
        Exception: if authentication fails.
    """
    try:
        mt_api = ThreadsAPI(username, password)
        return mt_api
    except Exception as e:
        logger.error("Threads authentication failed: %s", e)
        raise


def x_auth(x_keys):
    """
    Authenticate both versions of the X API.

    Args:
        x_keys: dictionary containing all required keys and tokens.

    Returns:
        Tuple containing authenticated API v1.1 and v2 objects.

    Raises:
        TweepyException: If authentication fails.
    """
    # X API v1.1 authentication and verification.
    x_oauth1 = OAuth1UserHandler(
        access_token_secret=x_keys["access_token_secret"],
        access_token=x_keys["access_token"],
        consumer_key=x_keys["consumer_key"],
        consumer_secret=x_keys["consumer_secret"],
    )
    x_api = XAPI(x_oauth1)
    try:
        x_api.verify_credentials()
    except TweepyException as e:
        logger.error("X API v1.1 authentication verification failed: %s", e)
        raise
    # X API v2 authentication and verification.
    x_cl = XClient(
        access_token_secret=x_keys["access_token_secret"],
        access_token=x_keys["access_token"],
        bearer_token=x_keys["bearer_token"],
        consumer_key=x_keys["consumer_key"],
        consumer_secret=x_keys["consumer_secret"],
        wait_on_rate_limit=True,
    )
    try:
        x_cl.get_me()
    except TweepyException as e:
        logger.error("X API v2 authentication verification failed: %s", e)
        raise
    return x_api, x_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
