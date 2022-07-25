# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import InvalidKeyError


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SET PYOB ATTR
# └─────────────────────────────────────────────────────────────────────────────────────


def set_pyob_attr(pyob, name, value):
    """Validates, indexes, and sets a PyOb instance attribute"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VARIABLES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get PyOb class
    PyObClass = pyob.__class__

    # Get PyObMeta
    PyObMeta = PyObClass.PyObMeta

    # Get store
    store = PyObMeta.store

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE KEY TYPE
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get keys
    keys = PyObClass.PyObMeta.keys or ()

    # Determine if key
    is_key = keys and name in keys

    # Check if key and is None
    if is_key and value is None:

        # Get PyOb class name
        class_name = PyObClass.__name__

        # Raise InvalidKeyError
        raise InvalidKeyError(
            f"{class_name}.{name} is a key and therefore cannot have a value of None"
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INDEX KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    # Check if is key
    if is_key:

        # Get PyObs instances by key
        pyobs_by_key = store._pyobs_by_key

        # Check previous value is defined
        # So that we can remove the existing key
        if name in pyob.__dict__:

            # Get previous value
            value_previous = pyob.__dict__[name]

            # Check if previous value is indexed
            if value_previous in pyobs_by_key:

                # Pop previous value from index
                pyobs_by_key.pop(value_previous)

        # Index new value as a key
        pyobs_by_key[value] = pyob
