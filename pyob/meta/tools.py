# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.meta.classes.metaclass_base import MetaclassBase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INITIALIZE PYOB META
# └─────────────────────────────────────────────────────────────────────────────────────


def initialize_pyob_meta(cls):
    """Initializes the PyObMeta class on a PyOb class"""

    # Get metaclass dictionary
    metaclass_dict = dict(MetaclassBase.__dict__)

    for Base in cls.__bases__:

        # Get PyObMeta of base class
        BasePyObMeta = getattr(Base, "PyObMeta", None)

        # Update metaclass dictionary
        BasePyObMeta and metaclass_dict.update(dict(BasePyObMeta.__dict__))

    # Update metaclass dictionary
    metaclass_dict.update(dict(cls.PyObMeta.__dict__))

    # Create a new reference for PyObMeta so each PyOb class has its own PyObMeta
    # Otherwise we will end up reassigning the mutable store on related PyOb classes
    cls.PyObMeta = type("PyObMeta", cls.PyObMeta.__bases__, pyob_meta_dict)

    """

    # Iterate over bases
    for base in cls.__bases__:

        # Get PyObMeta of base
        BasePyObMeta = getattr(base, "PyObMeta", None)

        # Update PyObMeta dictionary
        BasePyObMeta and pyob_meta_dict.update(dict(base.PyObMeta.__dict__))

    # Update PyObMeta dictionary
    pyob_meta_dict.update(dict(cls.PyObMeta.__dict__))

    # Create a new reference for PyObMeta so each PyOb class has its own PyObMeta
    # Otherwise we will end up reassigning the mutable store on related PyOb classes
    cls.PyObMeta = type("PyObMeta", cls.PyObMeta.__bases__, pyob_meta_dict)

    """
