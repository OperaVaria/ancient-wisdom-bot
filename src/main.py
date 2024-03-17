""" 
Main file of the "Ancient Wisdom Daily" project.

A Twitter bot that is set up to post a random
Ancient Greek or Roman quote of wisdom every day, with translation
and a short comment.

TODO: 1. Manual testing.
      2. Implement auto testing functions.
      3. Steadily add to database.
      4. Possibly implement different platforms.
"""

# Metadata variables:
__author__ = "OperaVaria"
__contact__ = "lcs_it@proton.me"
__version__ = "1.0.0"
__date__ = "2024.03.17"

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


# Imports:
import tweepy
from backend.assmbl_func import assemble_tweet
from auth.keys import (
    AWD_ACCESS_TOKEN_SECRET,
    AWD_ACCESS_TOKEN,
    AWD_BEARER_TOKEN,
    AWD_CONSUMER_KEY,
    AWD_CONSUMER_SECRET
)

# Set up API login.
client = tweepy.Client(
    access_token_secret=AWD_ACCESS_TOKEN_SECRET,
    access_token=AWD_ACCESS_TOKEN,
    bearer_token=AWD_BEARER_TOKEN,
    consumer_key=AWD_CONSUMER_KEY,
    consumer_secret=AWD_CONSUMER_SECRET,
    wait_on_rate_limit=True
)


def main():
    """Main function."""
    # Assemble tweet.
    tweet = assemble_tweet()
    # Post tweet.
    response = client.create_tweet(text=tweet)
    return response

# Launch main function.
if __name__ == "__main__":
    main()
