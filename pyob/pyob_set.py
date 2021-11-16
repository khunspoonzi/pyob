# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.mixins import PyObSetDunderMixin, PyObSetLabelMixin, PyObSetMethodMixin
from pyob.tools import convert_string_to_pascal_case


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB SET
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObSet(PyObSetLabelMixin, PyObSetDunderMixin, PyObSetMethodMixin):
    """A base class for PyOb object sets"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize object class to None
    _Ob = None

    # Initialize objects to None
    _obs = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, _Ob):
        """Init Method"""

        # Set object class
        self._Ob = _Ob

        # Initialize objects dict
        self._obs = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    def New(self):
        """Returns a new empty object set with the same object class"""

        # Return new object set
        return PyObSet(_Ob=self._Ob)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NAME
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def name(self):
        """Returns the name of the object set"""

        # Get the name based on the computed singular label
        name = self.label_singular

        # Convert name to Pascal case
        name = convert_string_to_pascal_case(name)

        # Return the name
        return name
