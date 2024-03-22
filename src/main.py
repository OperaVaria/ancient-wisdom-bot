"""
Main file of the "Ancient Wisdom Daily" project.

A multi-platform bot that is set up to post a random
Ancient Greek or Roman quote every day, with translation
and a short comment.

TODO: 1. Manual testing.
      2. Implement auto testing functions.
      3. Steadily add to database.
"""

# Metadata variables:
__author__ = "OperaVaria"
__contact__ = "lcs_it@proton.me"
__version__ = "1.0.0"
__date__ = "2024.03.22"

# Licence:
__license__ = "GPLv3"
__copyright__ = "Copyright © 2024, Csaba Latosinszky"

"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>
"""

# Imports from built-in modules:
from pathlib import Path
from os import remove as os_remove
from os.path import exists as os_exists

# Imports from external packages:
from tweepy import errors
from yaml import safe_load

# Imports from local modules:
from auth.auth_func import insta_login, threads_login, twitter_auth
from backend.assmbl_func import assemble_posts


def main():
    """Main function."""
    # Load authentication file.
    keys_path = Path(__file__).parents[0].resolve() / "auth/keys.yaml"
    with open(keys_path, "r", encoding="utf-8") as keys_file:
        keys = safe_load(keys_file)
    # Authenticate APIs
    in_cl = insta_login(keys)
    mt_api = threads_login(keys)
    tw_api, tw_cl = twitter_auth(keys)
    # Assemble posts.
    text_post, image_post = assemble_posts()
    # Temporarily save image post jpeg.
    temp_image_path = Path(__file__).parents[0].resolve() / "temp/post.jpg"
    image_post.image.save(temp_image_path,"JPEG")
    # Post tweet.
    try:
        tw_res = tw_cl.create_tweet(text=text_post)
    # If too long, post as picture.
    except errors.BadRequest:
        media_id = tw_api.media_upload(temp_image_path).media_id_string
        tw_res = tw_cl.create_tweet(text=image_post.caption, media_ids=[media_id])
    if tw_res:
        print("Twitter post successful!")
    else:
        print("Twitter posting failed!")
    # Post Instagram image.
    insta_res = in_cl.photo_upload(temp_image_path, image_post.caption)
    if insta_res:
        print("Instagram post successful!")
    else:
        print("Instagram posting failed!")
    # Post thread.
    mt_res = mt_api.publish(caption=text_post)
    if mt_res:
        print("Threads post successful!")
    else:
        print("Threads posting failed!")
    # Remove temp image.
    if os_exists(temp_image_path):
        os_remove(temp_image_path)
    return print("Process completed.")

# Launch main function.
if __name__ == "__main__":
    main()
