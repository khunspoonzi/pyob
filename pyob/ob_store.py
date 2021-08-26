# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.ob_set import ObSet


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB STORE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObStore(ObSet):
    """ A base class for PyOb object stores """

    # Initialize objects by key to None
    _obs_by_key = None

    # Initialize objects by unique field to None
    _obs_by_unique_field = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, *args, **kwargs):
        """ Init Method """

        # Call parent init method
        super().__init__(*args, **kwargs)

        # Initialize objects by key dict
        self._obs_by_key = {}

        # Initialize objects by unique field dict
        self._obs_by_unique_field = {}
