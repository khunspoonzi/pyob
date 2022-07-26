# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.main.tools.set_pyob_attr import set_pyob_attr  # noqa
from pyob.tools import is_pyob_base, is_pyob_subclass


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GET PYOB STRING FIELD
# └─────────────────────────────────────────────────────────────────────────────────────


def get_pyob_string_field(pyob):
    """Resolves and returns the best applicable string field for a PyOb instance"""

    # Initialize string field as PyObMeta.string
    # i.e. The field explicitly defined by the user
    string_field = pyob.PyObMeta.string

    # Default string field to the first available key if null
    # Provides a meaningful and unique string value for each PyOb
    string_field = string_field or (
        pyob.PyObMeta.keys[0] if pyob.PyObMeta.keys else None
    )

    # Return the string field
    return string_field


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
        if is_pyob_base(PyObClass) or not is_pyob_subclass(PyObClass):
            return PyObClass

        # Return if PyOb class in cache
        if PyObClass in cache:
            return cache[PyObClass]

        # Localize PyOb bases
        Bases = tuple([_localize(Base) for Base in PyObClass.__bases__])

        print("1")

        # Get and set localized PyOb class
        cache[PyObClass] = type(PyObClass.__name__, Bases, dict(PyObClass.__dict__))

        print("2")

        # Set localized from attribute
        # This will ensure that isinstance() still works with localized PyOb classes
        cache[PyObClass].PyObMeta.localized_from = PyObClass

        # Return the localized PyOb class
        return cache[PyObClass]

    # Localize PyOb classes
    PyObClasses = [_localize(PyObClass) for PyObClass in PyObClasses]

    # Return localized PyOb classes
    return PyObClasses[0] if len(PyObClasses) == 1 else tuple(PyObClasses)
