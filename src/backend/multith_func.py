"""
multith_func.py

Functions related to (pseudo-)multithreading.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging
from concurrent.futures import ThreadPoolExecutor

# Imports from local modules:
from backend.auth_func import bluesky_login, insta_login, mastodon_login, x_auth
from backend.post_func import bs_post, in_post, mt_post, x_post
from config.path_constants import INSTA_SESSION
from config.settings import INSTA_DELAY_RANGE

# Setup logging.
logger = logging.getLogger(__name__)


def threaded_login(keys):
    """
    Runs social media login functions concurrently 
    with the concurrent.futures module.
    
    Args:
        keys: login information dictionary.

    Returns:
        bs_cl, in_cl, mt_api, x_api, x_cl: authenticated
            social media Client and API objects.
    """
    # Executor context manager.
    with ThreadPoolExecutor(max_workers = 4) as executor:
        # Submit.
        bs_future = executor.submit(bluesky_login, keys["bluesky"]["handle"],
                                    keys["bluesky"]["password"])
        in_future = executor.submit(insta_login, keys["instagram"]["username"],
                                    keys["instagram"]["password"],
                                    INSTA_SESSION, INSTA_DELAY_RANGE)
        mt_future = executor.submit(mastodon_login, keys["mastodon"]["access_token"],
                                    keys["mastodon"]["api_base_uri"])
        x_future = executor.submit(x_auth, keys["x"])
        # Get Results.
        bs_cl = bs_future.result()
        in_cl = in_future.result()
        mt_api = mt_future.result()
        x_api, x_cl = x_future.result()
    return bs_cl, in_cl, mt_api, x_api, x_cl


def threaded_posting(bs_cl, in_cl, mt_api, x_api, x_cl,
                     text_post, image_post):
    """
    Runs social media posting functions concurrently 
    with the concurrent.futures module.
    
    Args:
        bs_cl, in_cl, mt_api, x_api, x_cl: authenticated
            social media Client and API objects.
        text_post: TextPost object.
        image_post: ImagePost object.
    
    Returns:
        bs_res, in_res, mt_res, x_res: request response objects.
    """
    with ThreadPoolExecutor(max_workers = 4) as executor:
        # Submit.
        bs_future = executor.submit(bs_post, bs_cl, image_post, text_post)
        in_future = executor.submit(in_post, in_cl, image_post, text_post)
        mt_future = executor.submit(mt_post, mt_api, text_post)
        x_future = executor.submit(x_post, x_api, x_cl, image_post, text_post)
        # Get Results.
        bs_res = bs_future.result()
        in_res = in_future.result()
        mt_res = mt_future.result()
        x_res = x_future.result()
    return bs_res, in_res, mt_res, x_res


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
