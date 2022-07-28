# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import re


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PASCALIZE
# └─────────────────────────────────────────────────────────────────────────────────────


def pascalize(string, delimiter=" "):
    """Converts a string to Pascal case"""

    # Split string
    string = [s.strip() for s in string.split(delimiter)]

    # Capitalize each word
    string = [s[0].upper() + s[1:] for s in string if s]

    # Join string
    string = "".join(string)

    # Return string
    return string


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SPLIT PASCAL
# └─────────────────────────────────────────────────────────────────────────────────────


def split_pascal(string):
    """Splits a string by Pascal case"""

    # Match string against Pascal case
    matches = re.finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", string
    )

    # Return string split by matches
    return [m.group(0) for m in matches]
