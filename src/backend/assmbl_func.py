"""
assmbl_func.py

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports from built-in modules:
import logging

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
        RuntimeError: If creation fails.
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


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
