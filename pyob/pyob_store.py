# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.pyob_set import PyObSet
from pyob.mixins import PyObStoreDunderMixin, PyObStoreMethodMixin


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStore(PyObStoreDunderMixin, PyObStoreMethodMixin, PyObSet):
    """A base class for PyOb object stores"""

    # Initialize objects by key to None
    _obs_by_key = None

    # Initialize objects by unique field to None
    _obs_by_unique_field = None

    # Initialize parents and children to None
    _parents = _children = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, *args, **kwargs):
        """Init Method"""

        # Call parent init method
        super().__init__(*args, **kwargs)

        # Initialize objects by key dict
        self._obs_by_key = {}

        # Initialize objects by unique field dict
        self._obs_by_unique_field = {}

        # Initialize parents and children
        self._parents, self._children = [], []

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POPULATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def populate(self):
        """Populates the object store based on a user-defined populate method"""

        # Call user-defined populate store method
        return self._Ob and self._Ob._populate_store()
