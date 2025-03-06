"""
post_func.py

Functions related to creating and publishing posts.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging

# Imports from external packages:
from atproto_client.exceptions import RequestException
from instagrapi.exceptions import ClientError
from tweepy import errors as tw_errors

# Local imports:
from backend.db_func import db_get
from backend.classes import ImagePost

# Setup logging:
logger = logging.getLogger(__name__)


def assemble_posts(db_file, image_size, bg_color, text_color,
                   reg_font, bold_font):
    """
    Function to assemble posts from Wisdom object data.

    Returns:
        Tuple containing text_post string and image_post object.

    Raises:
        RuntimeError: if creation fails.
    """
    try:
        # Get Wisdom object.
        wis_obj = db_get(db_file)
        # Log selected quote.
        logger.info("Quote selected: %s", wis_obj.id)
        # Call text post create method.
        text_post = wis_obj.create_text_post()
        # Create ImagePost instance.
        image_post = ImagePost(wis_obj, image_size, bg_color, text_color,
                               reg_font, bold_font)
        return text_post, image_post
    except RuntimeError as e:
        logger.error("Failed to assemble posts: %s", e)
        raise


def bs_post(bs_cl, text_post):
    """
    Post to Bluesky with error handling.

    Args:
        bs_cl: authenticated Bluesky client object.
        text_post: textual post string.
    
    Returns:
        bs_res: request response object.
    
    Raises:
        RequestException: if post request fails.
    """
    try:
        bs_res = bs_cl.send_post(text=text_post)
        return bs_res
    except RequestException as e:
        logger.error("Posting to Bluesky failed: %s", e)
        raise




def in_post(in_cl, image_post, temp_image_path):
    """
    Post to Instagram with error handling.

    Args:
        in_cl: authenticated Instagram client object.
        image_post: ImagePost object.
        temp_image_path: Path to the temporarily saved image post file.
    
    Returns:
        in_res: request response object.
           
    Raises:
        ClientError: if post request fails.
    """
    try:
        in_res = in_cl.photo_upload(temp_image_path, image_post.caption)
        return in_res
    except ClientError as e:
        logger.error("Posting to Instagram failed: %s", e)
        raise


def mt_post(mt_api, text_post):
    """
    Post to Meta Threads with error handling.

    Args:
        mt_api: authenticated Threads API object.
        text_post: textual post string.
    
    Returns:
        mt_res: request response object.
    
    Raises:
        Exception: if post request fails.
    """
    try:
        mt_res = mt_api.publish(caption=text_post)
        return mt_res
    except Exception as e:
        logger.error("Posting to Threads failed: %s", e)
        raise


def x_post(x_api, x_cl, text_post, image_post, image_temp_path):
    """
    Post text to X, if rejected (due to character length), try posting
    as image.

    Args:
        x_api, x_cl: authenticated X client and API objects.
        text_post: textual post string.
        image_post: ImagePost object.
        temp_image_path: Path to the temporarily saved image post file.

    Returns:
        x_res: request response object.

    Raises:
        TweepyException: if image post fallback fails.
    """
    try:
        # Attempt to post text.
        x_res = x_cl.create_tweet(text=text_post)
        return x_res
    except tw_errors.BadRequest:
        try:
            # Fall back to image.
            logger.info("Text posting failed. Falling back to image post")
            media_id = x_api.media_upload(image_temp_path).media_id_string
            x_res = x_cl.create_tweet(text=image_post.caption, media_ids=[media_id])
            return x_res
        except tw_errors.TweepyException as e:
            # Image fail: raise error.
            logger.error("Image posting to X failed: %s", e)
            raise


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
