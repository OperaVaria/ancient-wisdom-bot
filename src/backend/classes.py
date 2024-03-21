"""
classes.py

Classes used in the application.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Built-in imports:
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class Wisdom:
    """Quote data in Python object form."""
    def __init__(self, id_title, quote_orig, quote_eng, attrib_to,locus, locus_form, comment, used):
        """Create Wisdom object instance with attributes fetched from the database."""
        self.id = id_title
        self.original = quote_orig
        self.translation = quote_eng
        self.attribution = attrib_to
        self.locus = locus
        self.locus_formatted = locus_form
        self.comment = comment
        # Convert SQLite number to actual Boolean.
        self.used_value = bool(used)

    def create_text_post(self):
        """Assemble a test post form wisdom object data."""
        text_post = f'"{self.original}"\n"{self.translation}"\n/ {self.attribution} in {self.locus_formatted} /\n\n{self.comment}'
        return text_post

class ImagePost:
    """Instagram image post data in Python object form."""
    def __init__(self, wis_obj):
        """Create ImagePost instance from Wisdom object data."""
        # Create background image.
        quote_image = Image.new("RGB", (1080, 1080), (12, 4, 4))
        # Create an absolute path for font files.
        gentium_plus_reg = Path(__file__).parents[2].resolve() / "assets/fonts/Gentium_Plus/GentiumPlus-Regular.ttf"
        gentium_plus_bold = Path(__file__).parents[2].resolve() / "assets/fonts/Gentium_Plus/GentiumPlus-Bold.ttf"
        #Declare fonts:
        font_large_reg = ImageFont.truetype(gentium_plus_reg, 40)
        font_large_bold = ImageFont.truetype(gentium_plus_bold, 40)
        font_small_bold = ImageFont.truetype(gentium_plus_bold, 30)
        # Create wrapped text.
        text_origin = textwrap.fill(f'"{wis_obj.original}"', width=40)
        text_transl = textwrap.fill(f'"{wis_obj.translation}"', width=40)
        text_attrib = f"/ {wis_obj.attribution}\n In {wis_obj.locus} /"
        # Draw text on image.
        draw_cont = ImageDraw.Draw(quote_image)
        draw_cont.multiline_text(xy=(540, 384), text=text_origin, fill=(255, 255, 255),
                             font=font_large_bold, anchor="mm", align="center")
        draw_cont.multiline_text(xy=(540, 512), text=text_transl, fill=(255, 255, 255),
                             font=font_large_reg, anchor="mm", align="center")
        draw_cont.multiline_text(xy=(540, 768), text=text_attrib, fill=(255, 255, 255),
                             font=font_small_bold, anchor="mm", align="center")
        # Set attributes:
        self.image = quote_image
        self.caption = wis_obj.comment


# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
