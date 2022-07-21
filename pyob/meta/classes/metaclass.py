# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.meta.tools import initialize_pyob_meta


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class Metaclass(type):
    """The metaclass for the PyOb class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(cls, *args, **kwargs):
        """Init Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PYOB META
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize PyObMeta class
        initialize_pyob_meta(cls)
