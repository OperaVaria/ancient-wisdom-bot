"""
path_constants.py

File path constants.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Import.
from pathlib import Path


# Directories:
PROJECT_DIR = Path(__file__).parents[2].resolve()
ASSETS_DIR = PROJECT_DIR.joinpath("assets/")
FONT_DIR = ASSETS_DIR.joinpath("fonts/")
DB_DIR = PROJECT_DIR.joinpath("db/")
SRC_DIR = PROJECT_DIR.joinpath("src/")
CONFIG_DIR = SRC_DIR.joinpath("config/")
TEMP_DIR = SRC_DIR.joinpath("temp/")

# Files:
GENTIUM_REG_TTF = FONT_DIR.joinpath("Gentium_Plus/GentiumPlus-Regular.ttf")
GENTIUM_BOLD_TTF = FONT_DIR.joinpath("Gentium_Plus/GentiumPlus-Bold.ttf")
DB_FILE = DB_DIR.joinpath("wisdoms.db")
INSTA_SESSION = CONFIG_DIR.joinpath("session.json")
LOGIN_KEYS = CONFIG_DIR.joinpath("keys.yaml")
TEMP_DB_COPY = TEMP_DIR.joinpath("copy.db")
TEMP_POST_IMG = TEMP_DIR.joinpath("post.jpg")


# Print on accidental run:
if __name__ == "__main__":
    print("Config file. Not meant to be run!")
