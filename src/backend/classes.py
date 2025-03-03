"""
classes.py

Classes used in the application.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Built-in imports:
import logging
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Setup logging.
logger = logging.getLogger(__name__)

# Configuration constants
ASSETS_DIR = Path(__file__).parents[2].resolve() / "assets"
FONT_DIR = ASSETS_DIR / "fonts/Gentium_Plus"
DEFAULT_BG_COLOR = (12, 4, 4)
DEFAULT_TEXT_COLOR = (255, 255, 255)
DEFAULT_IMAGE_SIZE = (1080, 1080)


class Wisdom:
    """Quote data in Python object form."""

    def __init__(self, id_title, quote_orig, quote_eng,
                 attrib_to, locus, locus_form, comment, used):
        """Create Wisdom object instance with attributes fetched from the database."""
        self.id = id_title
        self.original = quote_orig
        self.translation = quote_eng
        self.attribution = attrib_to
        self.locus = locus
        self.locus_formatted = locus_form
        self.comment = comment
        self.used = bool(used)  # Convert SQLite number to actual Boolean.

    def create_text_post(self):
        """
        Assemble a text post from wisdom object data.

        Returns:
            text_post string.
        """
        text_post = (
            f'"{self.original}"\n"{self.translation}"\n'
            f"/ {self.attribution} in {self.locus_formatted} /\n\n{self.comment}"
        )
        return text_post


class ImagePost:
    """Instagram image post data in Python object form."""

    def __init__(self, wis_obj):
        """Create ImagePost instance from Wisdom object data."""
        self.caption = wis_obj.comment
        self.image = self.create_image(wis_obj)

    def create_image(self, wis_obj):
        """
        Create and return an image with the wisdom text.

        Returns:
            Image object.
        """
        # Create background image
        quote_image = Image.new("RGB", DEFAULT_IMAGE_SIZE, DEFAULT_BG_COLOR)
        # Load fonts
        font_large_reg, font_large_bold, font_small_bold = self._load_fonts()
        # Create wrapped text
        text_origin = textwrap.fill(f'"{wis_obj.original}"', width=40)
        text_transl = textwrap.fill(f'"{wis_obj.translation}"', width=40)
        text_attrib = f"/ {wis_obj.attribution}\n In {wis_obj.locus} /"
        # Draw text on image
        draw_cont = ImageDraw.Draw(quote_image)
        draw_cont.multiline_text(
            xy=(540, 384),
            text=text_origin,
            fill=DEFAULT_TEXT_COLOR,
            font=font_large_bold,
            anchor="mm",
            align="center",
        )
        draw_cont.multiline_text(
            xy=(540, 512),
            text=text_transl,
            fill=DEFAULT_TEXT_COLOR,
            font=font_large_reg,
            anchor="mm",
            align="center",
        )
        draw_cont.multiline_text(
            xy=(540, 768),
            text=text_attrib,
            fill=DEFAULT_TEXT_COLOR,
            font=font_small_bold,
            anchor="mm",
            align="center",
        )
        return quote_image

    def _load_fonts(self):
        """
        Helper method. Load and return fonts for image rendering.

        Returns:
            Large regular, large bold, small bold font objects.
        """
        try:
            gentium_reg = FONT_DIR / "GentiumPlus-Regular.ttf"
            gentium_bold = FONT_DIR / "GentiumPlus-Bold.ttf"

            font_large_reg = ImageFont.truetype(gentium_reg, 40)
            font_large_bold = ImageFont.truetype(gentium_bold, 40)
            font_small_bold = ImageFont.truetype(gentium_bold, 30)

            return font_large_reg, font_large_bold, font_small_bold
        except (FileNotFoundError, OSError) as e:
            # Fallback to default font if custom fonts aren't available
            print(f"Font loading error: {e}. Using default font.")
            return (ImageFont.load_default(),) * 3

    def save_image(self, path):
        """Save the image to the specified path."""
        self.image.save(path, "JPEG")


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
