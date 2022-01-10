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
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyOb Meta Class"""
