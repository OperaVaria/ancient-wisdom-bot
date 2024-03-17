"""
wisdom_class.py

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""


class Wisdom:
    """Quote data in Python object form."""
    def __init__(self, id_title, quote_orig, quote_eng, attrib_to, locus, comment, used):
        """Create Wisdom object instance with attributes fetched from the database."""
        self.id = id_title
        self.original = quote_orig
        self.translation = quote_eng
        self.attribution = attrib_to
        self.locus = locus
        self.comment = comment
        # Convert SQLite number to actual Boolean.
        self.used_value = bool(used)


# Print on accidental run:
if __name__ == '__main__':
    print("Importable module. Not meant to be run!")
