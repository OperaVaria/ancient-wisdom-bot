"""
auth_func.py

Functions for social media API authentication and login.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
from pathlib import Path
from os.path import exists as os_exists

# Imports from external packages:
from instagrapi import Client as InstaClient
from threadspy import ThreadsAPI
from tweepy import API as TwAPI
from tweepy import Client as TwClient
from tweepy import OAuth1UserHandler


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


def twitter_auth(keys):
    """Authenticate both versions of the Twitter API."""
    # Twitter API v1.1.
    tw_oauth1 = OAuth1UserHandler(
        access_token_secret=keys["twitter"]["access_token_secret"],
        access_token=keys["twitter"]["access_token"],
        consumer_key=keys["twitter"]["consumer_key"],
        consumer_secret=keys["twitter"]["consumer_secret"],
    )
    tw_api = TwAPI(tw_oauth1)
    # Twitter API v2.
    tw_cl = TwClient(
        access_token_secret=keys["twitter"]["access_token_secret"],
        access_token=keys["twitter"]["access_token"],
        bearer_token=keys["twitter"]["bearer_token"],
        consumer_key=keys["twitter"]["consumer_key"],
        consumer_secret=keys["twitter"]["consumer_secret"],
        wait_on_rate_limit=True,
    )
    return tw_api, tw_cl


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
