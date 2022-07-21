# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.meta.classes.metaclass_base import MetaclassBase
from pyob.store.classes import PyObStore
from pyob.tools.iterable import deduplicate


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

        # Get metaclass dictionary
        # i.e. A blank copy of the MetaclassBase attributes
        # To ensure every PyObMeta class shares a common set of attributes and methods
        metaclass_dict = dict(MetaclassBase.__dict__)

        # Update metaclass dictionary with the attributes of the current class PyObMeta
        # To ensure the metaclass dictionary inherits all the attributes and methods
        # defined in the current class PyObMeta
        metaclass_dict.update(dict(cls.PyObMeta.__dict__))

        # Create a new reference for PyObMeta so each PyOb class has its own PyObMeta
        # Otherwise we will end up reassigning mutable attributes such as the store
        cls.PyObMeta = type("PyObMeta", cls.PyObMeta.__bases__, metaclass_dict)

        # Get the freshly initialized PyObMeta
        PyObMeta = cls.PyObMeta

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RELATIVES
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize list of parent classes
        # i.e. The subset of bases that are also PyOb classes
        PyObMeta.Parents = []

        # Initialize list of child classes
        # i.e. Any PyOb classes that end up inheriting from the current class
        PyObMeta.Children = []

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize store
        # i.e. The "database" of all instances initialized from the current class
        PyObMeta.store = PyObStore(PyObClass=cls)

        # Iterate over all base classes
        for Base in cls.__bases__:

            # Get PyObMeta of base class
            # i.e. Most likely a PyOb class if PyObMeta is not None
            ParentPyObMeta = getattr(Base, "PyObMeta", None)

            # Get store of base PyObMeta class if not None
            parent_store = ParentPyObMeta and getattr(ParentPyObMeta, "store", None)

            # Continue if parent PyObMeta store is not a PyOb store
            # i.e. Definitely not a PyOb class
            if not isinstance(parent_store, PyObStore):
                continue

            # Add base class to Parents of current PyObMeta class
            PyObMeta.Parents.append(Base)

            # Add current class to Children of parent PyObMeta class
            ParentPyObMeta.Children.append(cls)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ KEYS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get keys from current PyObMeta
        keys = PyObMeta.keys or ()

        # Ensure that keys is a tuple
        # i.e. User can either pass in one key or an iterable of keys
        keys = keys and ((keys,) if type(keys) is str else tuple(keys))

        # Merge parent PyObMeta keys into current PyObMeta keys
        # This ensures that all PyOb subclasses inherit their parents' keys
        keys = sum([Parent.PyObMeta.keys for Parent in PyObMeta.Parents] + [keys], ())

        # Remove any duplicate keys
        keys = deduplicate(keys)

        # Set PyObMeta.keys
        PyObMeta.keys = keys

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ SUPER INIT
        # └─────────────────────────────────────────────────────────────────────────────

        # Call and return parent init method
        return super().__init__(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OBS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def obs(cls):
        """Returns the PyObStore of the current PyOb class"""

        # Return PyOb store
        return cls.PyObMeta.store
