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
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyOb Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize keys to None
        keys = None

        # Initialize unique fields to None
        unique = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ APPEARANCE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize display field to None
        display = None

        # Initialize labels to None
        label_singular = None
        label_plural = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RUNTIME SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize disable type checking to False
        disable_type_checking = False

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE STORE
        # └─────────────────────────────────────────────────────────────────────────────

        def populate_store(Class):
            """Populates the object store of a PyOb class"""

            # Return None
            return None

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
