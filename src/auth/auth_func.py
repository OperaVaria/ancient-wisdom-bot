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
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, LoginRequired
from threadspy import ThreadsAPI
from tweepy import API as XAPI
from tweepy import Client as XClient
from tweepy import OAuth1UserHandler

# Setup logging:
logger = logging.getLogger()

# Path constants:
INSTA_SETTINGS_PATH = Path(__file__).parents[0].resolve() / "settings.json"

# Login functions:

def bluesky_login(login, password):
    """Set up Bluesky login. Takes login data, returns client object."""
    bs_cl = BsClient()
    bs_cl.login(login, password)
    return bs_cl


def insta_login(username, password):
    """Set up Instagram login. Uses either username and password
    or previously saved session data. Takes login data, returns client object."""
    # Create Client instance.
    in_cl = InstaClient()
    # Add random delay to mimic live user interactions.
    in_cl.delay_range = [1, 3]
    # Load saved session settings if save file exists.
    session = in_cl.load_settings(INSTA_SETTINGS_PATH)
    # Declare login status booleans.
    login_via_session = False
    login_via_unp = False
    # If session exist, attempt to use it.
    if session:
        try:
            in_cl.set_settings(session)
            in_cl.login(username, password)
            # Check if session is valid
            try:
                in_cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password.")
                # Use the same device UUIDs across logins
                old_session = in_cl.get_settings()
                in_cl.set_settings({})
                in_cl.set_uuids(old_session["uuids"])
            # Set success boolean.
            login_via_session = True
        except ClientError as e:
            logger.info("Couldn't login user using session information: %s", e)
    # If not or unsuccessful: login via username and password.
    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. Username: %s", username)
            # If successful: set status boolean, dump session settings.
            if in_cl.login(username, password):
                login_via_unp = True
                in_cl.dump_settings(INSTA_SETTINGS_PATH)
        except ClientError as e:
            logger.info("Couldn't login user using username and password: %s", e)
    # Raise error if neither successful.
    if not login_via_unp and not login_via_session:
        raise ClientError("Login failed: couldn't login user with either password or session")
    # Return client object.
    return in_cl

def threads_login(username, password):
    """Set up Threads login. Takes login data, returns client object."""
    mt_api = ThreadsAPI(username, password)
    return mt_api


def x_auth(x_keys):
    """Authenticate both versions of the X API. Takes login data, returns client and API object."""
    # X API v1.1.
    x_oauth1 = OAuth1UserHandler(
        access_token_secret=x_keys["access_token_secret"],
        access_token=x_keys["access_token"],
        consumer_key=x_keys["consumer_key"],
        consumer_secret=x_keys["consumer_secret"],
    )
    x_api = XAPI(x_oauth1)
    # X API v2.
    x_cl = XClient(
        access_token_secret=x_keys["access_token_secret"],
        access_token=x_keys["access_token"],
        bearer_token=x_keys["bearer_token"],
        consumer_key=x_keys["consumer_key"],
        consumer_secret=x_keys["consumer_secret"],
        wait_on_rate_limit=True,
    )
    return x_api, x_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
