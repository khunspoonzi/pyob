# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.main.classes as pyob  # Protects against circular imports


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS PYOB
# └─────────────────────────────────────────────────────────────────────────────────────


def is_pyob(item):
    """Returns a boolean of whether an item is a PyOb instance"""

    # Return boolean of whether item is an Ob instance
    return isinstance(item, pyob.PyOb)
