# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import NonExistentKeyError
from pyob.main.tools.traverse import traverse_pyob_descendants
from pyob.set import PyObSet
from pyob.utils import Nothing, ReturnValue


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStore(PyObSet):
    """A base class for the primary PyOb set of a PyOb class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize PyObs by key to None
    _pyobs_by_key = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, *args, **kwargs):
        """Init Method"""

        # Call parent init method
        super().__init__(*args, **kwargs)

        # Initialize PyObs by key
        self._pyobs_by_key = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, key, default=Nothing):
        """Returns the PyOb associated with a key from the PyOb store"""

        # Define callback
        def callback(PyObClass):
            """Returns a PyOb instance by key if present"""

            # Get PyObMeta
            PyObMeta = PyObClass.PyObMeta

            # Get PyObs by key
            pyobs_by_key = PyObMeta.store._pyobs_by_key

            # Check if key in PyObs by key
            if key in pyobs_by_key:

                # Get PyOb instance
                pyob = pyobs_by_key[key]

                # Return PyOb instance in ReturnValue
                return ReturnValue(pyob)

        # Traverse PyOb descendants
        result = traverse_pyob_descendants(
            PyObClass=self._PyObClass, callback=callback, inclusive=True
        )

        # Extract PyOb instance from result
        pyob = result and result.value

        # Check if PyOb instance is not None
        if pyob is not None:

            # Return PyOb instance
            return pyob

        # Check if default is Nothing
        if default is Nothing:

            # Get singular label
            label_singular = self._PyObClass.label_singular

            # Check if key is a string
            if type(key) is str:

                # Add quotes to key for error message
                key = f"'{key}'"

            # Raise NonExistentKeyError
            raise NonExistentKeyError(
                f"A(n) {label_singular} instance with a key of {key} does not exist"
            )

        # Return default
        return default
