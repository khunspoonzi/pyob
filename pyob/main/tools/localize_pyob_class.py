# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.meta.classes.metaclass import Metaclass
from pyob.tools import is_pyob_base, is_pyob_subclass


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOCALIZE PYOB CLASS
# └─────────────────────────────────────────────────────────────────────────────────────


def localize_pyob_class(*PyObClasses):
    """Localizes and returns an interable of PyOb class instances"""

    # Initialize cache
    cache = {}

    # Define localize helper function
    def _localize(PyObClass):

        # Return if class is not a PyOb subclass
        if not is_pyob_subclass(PyObClass):
            return PyObClass

        # Return if PyOb class in cache
        if PyObClass in cache:
            return cache[PyObClass]

        # Localize PyOb bases
        Bases = tuple([_localize(Base) for Base in PyObClass.__bases__])

        # Get meta type
        # To ensure that Metaclass is copied into new PyOb class
        Type = Metaclass if is_pyob_base(PyObClass) else type

        # Get and set localized PyOb class
        cache[PyObClass] = Type(PyObClass.__name__, Bases, dict(PyObClass.__dict__))

        # Set localized from attribute
        # This will ensure that isinstance() still works with localized PyOb classes
        cache[PyObClass].PyObMeta.localized_from = PyObClass

        # Return the localized PyOb class
        return cache[PyObClass]

    # Localize PyOb classes
    PyObClasses = [_localize(PyObClass) for PyObClass in PyObClasses]

    # Return localized PyOb classes
    return PyObClasses[0] if len(PyObClasses) == 1 else tuple(PyObClasses)
