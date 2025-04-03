"""
settings.py

File containing configuration constants.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""


# Instagrapi settings.
INSTA_DELAY_RANGE = [1, 3]

# Image properties.
IMG_SIZE = (1080, 1080)
IMG_BG_COLOR = (12, 4, 4)
IMG_TEXT_COLOR = (255, 255, 255)


# Print on accidental run:
if __name__ == "__main__":
    print("Config file. Not meant to be run!")
