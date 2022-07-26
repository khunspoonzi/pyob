# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB SET
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObSet:
    """A base class for a collection of PyOb instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize PyOb class to None
    _PyObClass = None

    # Initialize counts by PyOb
    # i.e. A record of all PyOb instance counts in the PyObSet
    _counts_by_pyob = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, PyObClass):
        """Init Method"""

        # Set PyOb class
        self._PyObClass = PyObClass

        # Initialize counts by PyOb
        self._counts_by_pyob = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, key):
        """Get Item Method"""

        # Get by key
        return self.key(key)
