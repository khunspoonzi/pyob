# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import DuplicateKeyError, InvalidKeyError
from pyob.main.tools.index import index_pyob_attr
from pyob.main.tools.traverse import traverse_pyob_direct_relatives


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ VALIDATE PYOB ATTR
# └─────────────────────────────────────────────────────────────────────────────────────


def validate_pyob_attr(pyob, name, value):
    """Validates a PyOb instance attribute"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VARIABLES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get PyOb class
    PyObClass = pyob.__class__

    # Get PyObMeta
    PyObMeta = PyObClass.PyObMeta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE KEY TYPE
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get keys
    keys = PyObMeta.keys or ()

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


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ VALIDATE AND INDEX PYOB ATTR
# └─────────────────────────────────────────────────────────────────────────────────────


def validate_and_index_pyob_attr(pyob, name, value):
    """Validates and indexes a PyOb instance attribute"""

    # Validate PyOb instance attribute
    validate_pyob_attr(pyob=pyob, name=name, value=value)

    # Index PyOb instance attribute
    index_pyob_attr(pyob=pyob, name=name, value=value)
