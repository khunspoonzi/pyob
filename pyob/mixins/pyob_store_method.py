# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import NonExistentKeyError
from pyob.tools import traverse_pyob_descendants
from pyob.utils import Nothing, ReturnValue


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE METHOD MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreMethodMixin:
    """A mixin class for PyOb store methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, key, default=Nothing):
        """Returns the PyOb associated with a key from the PyOb set"""

        # Define callback
        def callback(PyObClass):
            """Returns a PyOb instance by key if present"""

            # Get PyObs by key
            _obs_by_key = PyObClass.PyObMeta.store._obs_by_key

            # Check if key in PyObs by key
            if key in _obs_by_key:

                # Get PyOb instance
                pyob = _obs_by_key[key]

                # Return PyOb instance in ReturnValue
                return ReturnValue(pyob)

        # Traverse PyOb descendants
        pyob = traverse_pyob_descendants(
            self._PyObClass,
            callback=callback,
            inclusive=True,
        )

        # Check if PyOb instance is not None
        if pyob is not None:

            # Return PyOb instance
            return pyob

        # Check if default is Nothing
        if default is Nothing:

            # Get PyOb label singular
            ob_label_singular = self.ob_label_singular

            # Check if key is a string
            if type(key) is str:

                # Add quotes to key for error message
                key = f"'{key}'"

            # Raise NonExistentKeyError
            raise NonExistentKeyError(
                f"A {ob_label_singular} instance with a key of {key} does not exist"
            )

        # Return default
        return default
