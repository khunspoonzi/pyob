# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.ob as ob
import pyob.ob_set as ob_set


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS ITERABLE
# └─────────────────────────────────────────────────────────────────────────────────────


def is_iterable(item):
    """ Returns a boolean of whether an item is iterable """

    # Return boolean of whether item is an iterable type
    return type(item) in [list, set, tuple, ob_set.ObSet]


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS OB
# └─────────────────────────────────────────────────────────────────────────────────────


def is_ob(item):
    """ Returns a boolean of whether an item is an Ob instance """

    # Return boolean of whether item is an Ob instance
    return isinstance(item, ob.Ob)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ IS OB SET
# └─────────────────────────────────────────────────────────────────────────────────────


def is_ob_set(item):
    """ Returns a boolean of whether an item is an ObSet instance """

    # Return boolean of whether item is an ObSet instance
    return isinstance(item, ob_set.ObSet)
