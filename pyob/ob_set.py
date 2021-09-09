# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.mixins import ObSetDunderMixin, ObSetLabelMixin, ObSetMethodMixin
from pyob.tools import convert_string_to_pascal_case


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSet(ObSetLabelMixin, ObSetDunderMixin, ObSetMethodMixin):
    """ A base class for PyOb object sets """

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
        """ Init Method """

        # Set object class
        self._Ob = _Ob

        # Initialize objects dict
        self._obs = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    def New(self):
        """ Returns a new empty object set with the same object class """

        # Return new object set
        return ObSet(_Ob=self._Ob)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def _keys(self):
        """ Returns the keys of the related object class if any """

        # Return object class keys
        return self._Ob._keys if self._Ob else None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NAME
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def name(self):
        """ Returns the name of the object set """

        # Get the name based on the computed singular label
        name = self.label_singular

        # Convert name to Pascal case
        name = convert_string_to_pascal_case(name)

        # Return the name
        return name
