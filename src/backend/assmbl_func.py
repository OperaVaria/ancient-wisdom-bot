"""
assmbl_func.py

Part of the "Ancient Wisdom Daily" project by OperaVaria.
"""

# Imports:
from backend.db_func import db_get


def assemble_tweet():
    """Function to create a tweet from Wisdom object data."""
    wis_obj = db_get()
    tweet = f'"{wis_obj.original}"\n"{wis_obj.translation}"\n/ {wis_obj.attribution} in {wis_obj.locus} /\n\n{wis_obj.comment}'
    return tweet


# Print on accidental run:
if __name__ == "__main__":
    print("Importable module. Not meant to be run!")
