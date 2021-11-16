# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.pyob_meta import PyObMeta
from pyob.pyob_set import PyObSet

from pyob.mixins import PyObDunderMixin, PyObLabelMixin
from pyob.tools import localize


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB
# └─────────────────────────────────────────────────────────────────────────────────────


class PyOb(PyObLabelMixin, PyObDunderMixin, metaclass=PyObMeta):
    """A base class for PyOb objects"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OBJECT SETTINGS
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize keys to None
    _keys = None

    # Initialize unique fields to None
    _unique = None

    # Initialize labels to None
    _label_singular = None
    _label_plural = None

    # Initialize string field to None
    _str = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RUNTIME SETTINGS
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize disable type checking to False
    _disable_type_checking = False

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOCALIZED
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def Localized(cls, include=None):
        """Returns a localized version of the PyOb class with an empty object store"""

        # Return localized classes
        return localize(cls, *(include or []))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SET
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def Set(cls):
        """Initializes a new PyOb object set for the current PyOb object class"""

        # Return the initialized object set
        return PyObSet(_Ob=cls)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _POPULATE STORE
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def _populate_store(cls):
        """Populates the object store of a PyOb class"""

        # Return None
        return None
