# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.main.classes as pyob  # Protects against circular imports


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS PYOB BASE
# └─────────────────────────────────────────────────────────────────────────────────────


def is_pyob_base(Class):
    """Returns a boolean of whether a class is PyOb"""

    # Return boolean of whether class is PyOb
    return Class is pyob.PyOb


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS PYOB INSTANCE
# └─────────────────────────────────────────────────────────────────────────────────────


def is_pyob_instance(item):
    """Returns a boolean of whether an item is a PyOb instance"""

    # Return boolean of whether item is a PyOb instance
    return isinstance(item, pyob.PyOb)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS PYOB SUBCLASS
# └─────────────────────────────────────────────────────────────────────────────────────


def is_pyob_subclass(Class):
    """Returns a boolean of whether a class is a subclass of PyOb"""

    # Return boolean of whether class is a subclass of PyOb
    return issubclass(Class, pyob.PyOb)
