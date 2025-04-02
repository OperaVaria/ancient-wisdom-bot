"""
classes.py

Classes used in the application.

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Built-in imports:
import logging
import textwrap
from dataclasses import dataclass

# Imports from external packages:
from PIL import Image, ImageDraw, ImageFont

# Setup logging.
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Wisdom:
    """
    Quote data in Python dataclass object form.
    Filled up by tuple with information retrieved from database.
    """
    id: str
    original: str
    translation: str
    attribution: str
    locus: str
    locus_formatted: str
    comment: str
    used: bool


class TextPost:
    """Social media textual post factory in Python object form."""

    def __init__(self, wisdom_obj):
        """
        Assemble text post strings needed for social media posting
        from Wisdom object data.
        """
        self.full_text = (
            f'"{wisdom_obj.original}"\n"{wisdom_obj.translation}"\n'
            f"/ {wisdom_obj.attribution} in {wisdom_obj.locus_formatted} /"
            f"\n\n{wisdom_obj.comment}"
        )
        self.accessibility_text = (
            f'Original quote: "{wisdom_obj.original}"\n'
            f'Translation: "{wisdom_obj.translation}"\n'
            f'Source: "{wisdom_obj.attribution} in {wisdom_obj.locus_formatted}"'
        )
        self.comment_text = wisdom_obj.comment


class ImagePost:
    """Social media image post data and factory in Python object form."""

    def __init__(self, wis_obj, image_size, bg_color, text_color,
                 reg_font, bold_font):
        """Create ImagePost instance from Wisdom object data
        and image attributes."""
        self.size = image_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.reg_font = reg_font
        self.bold_font = bold_font
        self.path = None
        # Call create_image method.
        self.image = self.create_image(wis_obj)

    def create_image(self, wis_obj):
        """
        Create and return an image with the wisdom text.

        Args:
            wis_obj: Wisdom class instance.

        Returns:
            Image object.
        """
        # Create background image.
        quote_image = Image.new("RGB", self.size, self.bg_color)
        # Load fonts with helper method.
        font_large_reg, font_large_bold, font_small_bold = self._load_fonts()
        # Create wrapped text.
        text_origin = textwrap.fill(f'"{wis_obj.original}"', width=40)
        text_transl = textwrap.fill(f'"{wis_obj.translation}"', width=40)
        text_attrib = f"/ {wis_obj.attribution}\n In {wis_obj.locus} /"
        # Draw text on image.
        draw_cont = ImageDraw.Draw(quote_image)
        draw_cont.multiline_text(
            xy=(540, 384),
            text=text_origin,
            fill=self.text_color,
            font=font_large_bold,
            anchor="mm",
            align="center",
        )
        draw_cont.multiline_text(
            xy=(540, 512),
            text=text_transl,
            fill=self.text_color,
            font=font_large_reg,
            anchor="mm",
            align="center",
        )
        draw_cont.multiline_text(
            xy=(540, 768),
            text=text_attrib,
            fill=self.text_color,
            font=font_small_bold,
            anchor="mm",
            align="center",
        )
        return quote_image

    def _load_fonts(self):
        """
        Helper method for create_image.
        Load and return fonts for image rendering.
        Load ImageFont default with error message if custom font unavailable.

        Returns:
            Large regular, large bold, small bold font objects.
        """
        # Declare font variables.
        font_large_reg = None
        font_large_bold = None
        font_small_bold = None
        try:
            # Try loading the custom fonts.
            font_large_reg = ImageFont.truetype(self.reg_font, 40)
            font_large_bold = ImageFont.truetype(self.bold_font, 40)
            font_small_bold = ImageFont.truetype(self.bold_font, 30)
        except FileNotFoundError:
            logger.error("Font file not found. Using default font")
            font_large_reg = ImageFont.load_default()
            font_large_bold = ImageFont.load_default()
            font_small_bold = ImageFont.load_default()
        except OSError as e:
            logger.error("Font loading error: %s. Using default font", e)
            font_large_reg = ImageFont.load_default()
            font_large_bold = ImageFont.load_default()
            font_small_bold = ImageFont.load_default()

        return font_large_reg, font_large_bold, font_small_bold

    def save_image(self, path):
        """Save the image to a specified path."""
        self.image.save(path, "JPEG")
        self.path = path

    def open_bin(self):
        """
        Open saved image as binary

        Returns:
            Binary image data.
        
        Raises:
            TypeError: Image has not been saved yet (=None).
        """
        if self.path is None:
            raise TypeError("self.path is None, image path unknown")

        with open(self.path, "rb") as file:
            bin_data = file.read()
            return bin_data


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
