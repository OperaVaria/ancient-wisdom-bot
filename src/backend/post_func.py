"""
post_func.py

Functions related to creating and publishing posts.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging

# Imports from external packages:
from atproto_client.exceptions import BadRequestError
from atproto_client.exceptions import RequestException
from instagrapi.exceptions import ClientBadRequestError
from mastodon.errors import MastodonAPIError
from tweepy.errors import BadRequest, Forbidden

# Local imports:
from backend.db_func import db_get
from backend.classes import TextPost, ImagePost

# Setup logging:
logger = logging.getLogger(__name__)


def assemble_posts(db_file, image_size, bg_color, text_color,
                   reg_font, bold_font):
    """
    Function to assemble posts from Wisdom object data.

    Returns:
        Tuple containing TextPost and ImagePost object.

    Raises:
        RuntimeError: if creation fails.
    """
    try:
        # Get Wisdom object.
        wis_obj = db_get(db_file)
        # Log selected quote.
        logger.info("Quote selected: %s", wis_obj.id)
        # Call text post create method.
        text_post = TextPost(wis_obj)
        # Create ImagePost instance.
        image_post = ImagePost(wis_obj, image_size, bg_color, text_color,
                               reg_font, bold_font)
        return text_post, image_post
    except RuntimeError as e:
        logger.error("Failed to assemble posts: %s", e)
        raise


def bluesky_post(bs_cl, image_post, text_post):
    """
    Post to Bluesky, if rejected (due to character length), try posting
    as image.

    Args:
        bs_cl: authenticated Bluesky client object.
        image_post: ImagePost object.
        text_post: TextPost object.
    
    Returns:
        bs_res: request response object.
    
    Raises:
        RequestException: if post request fails.
    """
    try:
        # Attempt to post text.
        bs_res = bs_cl.send_post(text=text_post.full_text)
        return bs_res
    except BadRequestError:
        try:
            # Fall back to image.
            logger.info("Text posting to Bluesky failed. Falling back to image post")
            bs_res = bs_cl.send_image(text=text_post.comment_text, image=image_post.open_bin(),
                                      image_alt=text_post.accessibility_text)
            return bs_res
        except RequestException as e:
            # Image fail: raise error.
            logger.error("Image posting to Bluesky failed: %s", e)
            raise


def insta_post(in_cl, image_post, text_post):
    """
    Post to Instagram with error handling.

    Args:
        in_cl: authenticated Instagram client object.
        image_post: ImagePost object.
        text_post: TextPost object.
    
    Returns:
        in_res: request response object.
           
    Raises:
        ClientBadRequestError: if post request fails.
    """
    try:
        in_res = in_cl.photo_upload(
            path=image_post.path,
            caption=text_post.comment_text,
            extra_data={"custom_accessibility_caption": text_post.accessibility_text},
        )
        return in_res
    except ClientBadRequestError as e:
        logger.error("Posting to Instagram failed: %s", e)
        raise


def mastodon_post(mt_api, image_post, text_post):
    """
    Post text to Mastodon, if rejected (due to character length), try posting
    as image.

    Args:
        mt_api: authenticated Mastodon API object.
        image_post: ImagePost object.
        text_post: TextPost object.
    
    Returns:
        mt_res: request response object.
    
    Raises:
        MastodonAPIError: if image post fallback fails.
    """
    try: # Attempt to post text.
        mt_res = mt_api.status_post(status=text_post.full_text,
                                  visibility="public")
        return mt_res
    except MastodonAPIError:
        try: # Fall back to image.
            logger.info("Text posting to X failed. Falling back to image post")
            media = mt_api.media_post(media_file=image_post.path,
                                    description=text_post.accessibility_text)
            mt_res = mt_api.status_post(status=text_post.full_text,
                                        media_ids=[media["id"]],
                                        visibility="public")
            return mt_res
        except MastodonAPIError as e:
            # Image fail: raise error.
            logger.error("Image posting to Mastodon failed: %s", e)
            raise


def x_post(x_api, x_cl, image_post, text_post):
    """
    Post text to X, if rejected (due to character length), try posting
    as image.

    Args:
        x_api, x_cl: authenticated X client and API objects.        
        image_post: ImagePost object.
        text_post: TextPost object.

    Returns:
        x_res: request response object.

    Raises:
        BadRequest: if image post fallback fails.
    """
    try:
        # Attempt to post text.
        x_res = x_cl.create_tweet(text=text_post.full_text)
        return x_res
    except Forbidden:
        try:
            # Fall back to image.
            logger.info("Text posting to X failed. Falling back to image post")
            media = x_api.media_upload(filename=image_post.path, media_category="tweet_image")
            x_res = x_cl.create_tweet(text=text_post.comment_text, media_ids=[media.media_id])
            return x_res
        except BadRequest as e:
            # Image fail: raise error.
            logger.error("Image posting to X failed: %s", e)
            raise


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
