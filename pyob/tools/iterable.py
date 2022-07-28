# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.set import PyObSet


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DEDUPLICATE
# └─────────────────────────────────────────────────────────────────────────────────────


def deduplicate(iterable, recursive=False):
    """Removes duplcates from an iterable while preserving its order"""

    # Determine iterable cast function
    # i.e. The callable type of the passed in iterable
    to_type = type(iterable)

    # Initialize seen set
    # i.e. The set we use to identify diplicate items
    seen = set()
    see = seen.add

    # Remove duplicates items from iterable
    iterable = [
        deduplicate(i, recursive=recursive) if recursive and is_iterable(i) else i
        for i in iterable
        if not (i in seen or see(i))
    ]

    # Return iterable of unique items
    return to_type(iterable)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS ITERABLE
# └─────────────────────────────────────────────────────────────────────────────────────


def is_iterable(item):
    """Returns a boolean of whether or not an item is iterable"""

    # Return boolean of whether or not item is an iterable
    return type(item) in [list, set, tuple, PyObSet]
