# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INDEX PYOB ATTR
# └─────────────────────────────────────────────────────────────────────────────────────


def index_pyob_attr(pyob, name, value):
    """Indexes a PyOb instance attribute in the PyOb store"""

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
    # │ INDEX KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get keys
    keys = PyObMeta.keys or ()

    # Determine if key
    is_key = keys and name in keys

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
