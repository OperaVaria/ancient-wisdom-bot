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
from datetime import datetime, timedelta
from backend.assmbl_func import assemble_tweet
from auth.keys import (
    awd_access_token_secret,
    awd_access_token,
    awd_bearer_token,
    awd_consumer_key,
    awd_consumer_secret
)

# Set up API login.
client = tweepy.Client(
    access_token_secret=awd_access_token_secret,
    access_token=awd_access_token,
    bearer_token=awd_bearer_token,
    consumer_key=awd_consumer_key,
    consumer_secret=awd_consumer_secret,
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
