# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import DuplicateKeyError, InvalidKeyError
from pyob.main.tools.traverse import traverse_pyob_direct_relatives


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
    # │ TRAVERSE PYOB RELATIVES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define traversal callback
    def callback(PyObClass):
        """Validates a PyOb instance attribute against its PyOb class relatives"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ VARIABLES
        # └─────────────────────────────────────────────────────────────────────────────

        # Get PyObMeta
        PyObMeta = PyObClass.PyObMeta

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ VALIDATE KEY UNICITY
        # └─────────────────────────────────────────────────────────────────────────────

        # Check if is a key in the PyOb class
        if is_key and name in PyObMeta.keys:

            # Get PyObs by key map
            pyobs_by_key = PyObMeta.store._pyobs_by_key

            # Check if value in PyObs by key map
            if value in pyobs_by_key:

                # Get other
                other = pyobs_by_key[value]

                # Check if existing index is not the current PyOb instance
                if id(other) != id(pyob):

                    # Get singular label
                    label_singular = PyObClass.label_singular

                    # Raise DuplicateKeyError
                    raise DuplicateKeyError(
                        f"A {label_singular} with a key of {value} already exists: "
                        f"{other}"
                    )

    # Traverse PyOb direct relatives
    traverse_pyob_direct_relatives(
        PyObClass=PyObClass, callback=callback, inclusive=True
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
