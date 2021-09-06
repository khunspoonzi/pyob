# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.ob_meta import ObMeta
from pyob.ob_set import ObSet

from pyob.mixins import ObDunderMixin, ObLabelMixin
from pyob.tools import localize


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB
# └─────────────────────────────────────────────────────────────────────────────────────


class Ob(ObLabelMixin, ObDunderMixin, metaclass=ObMeta):
    """ A base class for PyOb objects """

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
    def _populate_store(cls):
        """ Populates the object store of a PyOb class """

        # Return
        return

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOCALIZED
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def Localized(cls, include=None):
        """ Returns a localized version of the PyOb class with an empty object store """

        # Return localized classes
        return localize(cls, *(include or []))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SET
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def Set(cls):
        """ Initializes a new PyOb object set for the current PyOb object class """

        # Return the initialized object set
        return ObSet(_Ob=cls)
