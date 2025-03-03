"""
auth_func.py

Functions for social media API authentication and login.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging
from pathlib import Path

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

# Path constants:
DEFAULT_SETTINGS_DIR = Path(__file__).parent
INSTA_SETTINGS_PATH = DEFAULT_SETTINGS_DIR / "settings.json"
INSTA_DELAY_RANGE = [1, 3]

# Login functions:

def bluesky_login(login, password):
    """
    Set up Bluesky login.

    Args:
        login: Bluesky username
        password: Bluesky password.

    Returns:
        BsClient: Authenticated Bluesky client object.

    Raises:
        Exception: If login fails.
    """
    bs_cl = BsClient()
    try:
        bs_cl.login(login, password)
        logger.info("Successfully logged in to Bluesky as %s", login)
        return bs_cl
    except AtProtocolError as e:
        logger.error("Bluesky login failed: %s", e)
        raise


def insta_login(username, password, settings_path=INSTA_SETTINGS_PATH):
    """
    Set up Instagram login using either username and password
    or previously saved session data.

    Args:
        username: Instagram username.
        password: Instagram password.
        settings_path: Path to session settings (default: INSTA_SETTINGS_PATH constant).

    Returns:
        InstaClient: Authenticated Instagram client object.

    Raises:
        ClientError: If login fails with both methods.
    """
    # Create Client instance.
    in_cl = InstaClient()
    # Add random delay to mimic live user interactions.
    in_cl.delay_range = INSTA_DELAY_RANGE
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
    session = client.load_settings(settings_path)
    if not session:
        return False
    # Attempt login with error handling.
    try:
        client.set_settings(session)
        client.login(username, password)
        # Verify if session is valid.
        try:
            client.get_timeline_feed()
            logger.info(
                "Successfully logged in to Instagram as %s, using previously saved session.",
                username,
            )
            return True
        # If not, raise exception.
        except LoginRequired:
            logger.error("Session is invalid, need to login via username and password.")
            # Preserve device UUIDs across logins
            old_session = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            return False
    except ClientError as e:
        logger.error("Couldn't login user using session information: %s.", e)
        return False


def _try_credentials_login(client, username, password, settings_path):
    """Helper function for insta_login to attempt login via username and password."""
    try:
        logger.info(
            "Attempting to login via username and password. Username: %s.", username
        )
        if client.login(username, password):
            logger.info(
                "Successfully logged in to Instagram as %s using credentials.", username
            )
            client.dump_settings(settings_path)
            return True
        return False
    except ClientError as e:
        logger.error("Couldn't login user using username and password: %s.", e)
        return False


def threads_login(username, password):
    """
    Set up Threads login.

    Args:
        username: Threads username.
        password: Threads password.

    Returns:
        ThreadsAPI: Authenticated Threads API object.
    """
    mt_api = ThreadsAPI(username, password)
    return mt_api


def x_auth(x_keys):
    """
    Authenticate both versions of the X API.

    Args:
        x_keys: dictionary containing all required keys and tokens.

    Returns:
        Tuple containing authenticated API v1.1 and v2 objects.

    Raises:
        tweepy.errors.TweepyException: If authentication fails.
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
        logger.info("Successfully authenticated X API v1.1.")
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
        logger.info("Successfully authenticated X API v2")
    except TweepyException as e:
        logger.error("X API v2 authentication verification failed: %s", e)
        raise
    return x_api, x_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
