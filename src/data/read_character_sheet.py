import os
import re

from src.data.models.dnd_beyond_sheet import DNDBeyondExtractedCharacterData


def _safe_key(key: str) -> str:
    return key.strip().replace(" ", "")


def extract_character_details():
    # Tried PyPDF2, but was hitting a bit of a wall. CAn consistently parse the key / value
    # pairs with this pattern, but probably a bit flimsy
    value_pair_regex = r"\/T\((.*)\)\n\/Type\/Annot\n\/V\((.*)\)"

    path = os.getcwd()
    file_name = f"{path}/src/data/character_sheets/price1847_7693867.pdf"

    with open(file_name, encoding="utf-8", errors="ignore") as f:
        file_contents = f.read()
        pairs = re.findall(value_pair_regex, file_contents, re.IGNORECASE)
        character_details = {_safe_key(k): v.strip() for k, v in pairs}
        return DNDBeyondExtractedCharacterData(**character_details)


if __name__ == "__main__":
    extract_character_details()
