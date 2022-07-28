# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.main.tools.localize import localize_pyob_class  # noqa


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GET PYOB STRING FIELD
# └─────────────────────────────────────────────────────────────────────────────────────


def get_pyob_string_field(pyob):
    """Resolves and returns the best applicable string field for a PyOb instance"""

    # Initialize string field as PyObMeta.string
    # i.e. The field explicitly defined by the user
    string_field = pyob.PyObMeta.string

    # Default string field to the first available key if null
    # Provides a meaningful and unique string value for each PyOb
    string_field = string_field or (
        pyob.PyObMeta.keys[0] if pyob.PyObMeta.keys else None
    )

    # Return the string field
    return string_field
