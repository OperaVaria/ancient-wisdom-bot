"""
Main file of the "Ancient Wisdom Daily" project.

A multi-platform bot that is set up to post a random
Ancient Greek or Roman quote every day, with translation
and a short comment.

TODO: 1. Steadily add to database.
"""

# Imports from built-in modules:
import logging
from os import remove as os_remove
from os.path import exists as os_exists

# Imports from external packages:
from yaml import safe_load

# Imports from local modules:
from backend.multith_func import threaded_login, threaded_posting
from backend.post_func import assemble_posts
from config.path_constants import (DB_FILE, GENTIUM_REG_TTF, GENTIUM_BOLD_TTF,
                                   LOGIN_KEYS, TEMP_POST_IMG)
from config.settings import IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR


# Metadata variables:
__author__ = "OperaVaria"
__contact__ = "lcs_it@proton.me"
__version__ = "2.1.0"
__date__ = "2025.05.08"

# Licence:
__license__ = "GPLv3"
__copyright__ = "Copyright © 2025, Csaba Latosinszky"

"""
This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>
"""

# Setup logging:
logger = logging.getLogger(__name__)


def main():
    """
    Main function.
    
    Returns:
        Exit code.
    """
    # Configure logging.
    logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s.", level=logging.INFO
    )
    # Load authentication file with error handling.
    try:
        with open(LOGIN_KEYS, "r", encoding="utf-8") as keys_file:
            keys = safe_load(keys_file)
    except (FileNotFoundError, PermissionError) as e:
        logger.critical("Failed to load authentication keys: %s", e)
        return 1
    # Authenticate APIs concurrently.
    bs_cl, in_cl, mt_api, x_api, x_cl = threaded_login(keys)
    # Assemble posts.
    text_post, image_post = assemble_posts(DB_FILE, IMG_SIZE, IMG_BG_COLOR, IMG_TEXT_COLOR,
                                           GENTIUM_REG_TTF, GENTIUM_BOLD_TTF)
    # Temporarily save image post jpeg.
    image_post.save_image(TEMP_POST_IMG)
    # Post concurrently.
    threaded_posting(bs_cl, in_cl, mt_api, x_api, x_cl,
                     text_post, image_post)
    # Remove temp image with error handling,
    if os_exists(TEMP_POST_IMG):
        try:
            os_remove(TEMP_POST_IMG)
        except OSError as e:
            logger.error("Failed to remove temporary image: %s", e)
    logger.info("Process completed")
    return 0


# Launch main function.
if __name__ == "__main__":
    main()
