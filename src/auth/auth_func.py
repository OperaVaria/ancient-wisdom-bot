"""
auth_func.py

Functions for social media API authentication and login.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from pathlib import Path
from os.path import exists as os_exists

# Imports from external packages:
from atproto import Client as BsClient
from instagrapi import Client as InstaClient
from threadspy import ThreadsAPI
from tweepy import API as XAPI
from tweepy import Client as XClient
from tweepy import OAuth1UserHandler

# Login functions:

def bluesky_login(keys):
    """Set up Bluesky login."""
    bs_cl = BsClient()
    bs_cl.login(login=keys["bluesky"]["handle"], password=keys["bluesky"]["password"])
    return bs_cl


def insta_login(keys):
    """Set up Instagram login."""
    # Create Client instance.
    in_cl = InstaClient()
    # Load settings.
    settings_path = Path(__file__).parents[0].resolve() / "settings.json"
    if os_exists(settings_path):
        in_cl.load_settings(settings_path)
    else:
        in_cl.dump_settings(settings_path)
    # Login.
    in_cl.login(username=keys["meta"]["username"], password=keys["meta"]["password"])
    return in_cl


def threads_login(keys):
    """Set up Threads login."""
    mt_api = ThreadsAPI(keys["meta"]["username"], keys["meta"]["password"])
    return mt_api


def x_auth(keys):
    """Authenticate both versions of the X API."""
    # X API v1.1.
    x_oauth1 = OAuth1UserHandler(
        access_token_secret=keys["x"]["access_token_secret"],
        access_token=keys["x"]["access_token"],
        consumer_key=keys["x"]["consumer_key"],
        consumer_secret=keys["x"]["consumer_secret"],
    )
    x_api = XAPI(x_oauth1)
    # X API v2.
    x_cl = XClient(
        access_token_secret=keys["x"]["access_token_secret"],
        access_token=keys["x"]["access_token"],
        bearer_token=keys["x"]["bearer_token"],
        consumer_key=keys["x"]["consumer_key"],
        consumer_secret=keys["x"]["consumer_secret"],
        wait_on_rate_limit=True,
    )
    return x_api, x_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
