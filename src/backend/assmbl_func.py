"""
assmbl_func.py

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Local imports:
from backend.db_func import db_get
from backend.classes import ImagePost


def assemble_posts():
    """Function to assemble posts from Wisdom object data."""
    # Get Wisdom object.
    wis_obj = db_get()
    # Print selected quote.
    print(f"Quote selected: {wis_obj.id}")
    # Call text post create method.
    text_post = wis_obj.create_text_post()
    # Create ImagePost instance.
    image_post = ImagePost(wis_obj)
    return text_post, image_post


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
