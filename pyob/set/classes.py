# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.tools.string import pascalize


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

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self):
        """Iterate Method"""

        # Iterate over counts by PyOb
        for pyob, count in self._counts_by_pyob.items():

            # Iterate over count
            for _ in range(count):

                # Yield PyOb
                yield pyob

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self):
        """Length Method"""

        # Return sum of counts by PyOb
        return sum(self._counts_by_pyob.values())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self):
        """Representation Method"""

        # Define threshold
        threshold = 20

        # Get PyOb count
        pyob_count = len(self)

        # Initialize representation to singular label
        representation = self._PyObClass.label_singular

        # Ensure representation is in Pascal case
        representation = pascalize(representation)

        # Add count to representation
        representation += f": {pyob_count}"

        # Initialize PyObs
        pyobs = []

        # Iterate over PyOb set
        # NOTE: __iter__ is a generator so better we don't call list(self)
        for pyob in self:

            # Break if length of PyObs is greater than or equal to threshold
            if len(pyobs) >= threshold:
                break

            # Append stringified PyOb to PyObs
            pyobs.append(pyob.__repr__())

        # Check if there are more than n PyObs total
        if pyob_count > threshold:

            # Add truncation message to PyObs list
            pyobs.append("...(remaining elements truncated)... ")

        # Add stringified PyObs to representation
        representation = f"{representation} {'[' + ', '.join(pyobs) + ']'}"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation
