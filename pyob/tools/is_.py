# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.pyob as pyob
import pyob.pyob_set as pyob_set


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS ITERABLE
# └─────────────────────────────────────────────────────────────────────────────────────


def is_iterable(item):
    """Returns a boolean of whether an item is iterable"""

    # Return boolean of whether item is an iterable type
    return type(item) in [list, set, tuple, pyob_set.PyObSet]


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS OB
# └─────────────────────────────────────────────────────────────────────────────────────


def is_ob(item):
    """Returns a boolean of whether an item is an Ob instance"""

    # Return boolean of whether item is an Ob instance
    return isinstance(item, pyob.PyOb)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS OB SET
# └─────────────────────────────────────────────────────────────────────────────────────


def is_ob_set(item):
    """Returns a boolean of whether an item is an ObSet instance"""

    # Return boolean of whether item is an ObSet instance
    return isinstance(item, pyob_set.PyObSet)
