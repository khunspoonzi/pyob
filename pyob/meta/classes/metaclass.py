# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.meta.classes.metaclass_base import MetaclassBase
from pyob.store.classes import PyObStore
from pyob.tools.iterable import deduplicate
from pyob.tools.string import split_pascal


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
        # │ ATTRIBUTE INHERITANCE
        # └─────────────────────────────────────────────────────────────────────────────

        # Define inheritable attributes
        # i.e. Attributes that will inherit from the first parent if not set otherwise
        inheritable_attributes = ("string",)

        # Iterate over inheritable attributes
        for inheritable_attribute in inheritable_attributes:

            # Get the value of the inheritable attribute
            inheritable_attribute_value = getattr(PyObMeta, inheritable_attribute, None)

            # Continue if the value of the inheritable attribute is not None
            # i.e. It has been set explicitly and therefore should not be touched
            if inheritable_attribute_value is not None:
                continue

            # Iterate over parent classes
            for Parent in PyObMeta.Parents:

                # Get the PyObMeta of the parent class
                ParentPyObMeta = Parent.PyObMeta

                # Get inherited attribute value from parent PyObMeta
                inherited_attribute_value = getattr(
                    ParentPyObMeta, inheritable_attribute, None
                )

                # Continue if the inherited attribute value is None
                # i.e. No meaningful attribute value to inherit
                if inherited_attribute_value is None:
                    continue

                # Set the inherited value on the current PyOb class and break
                # i.e. Inherit the first meaningful attribute from any of the parents
                setattr(PyObMeta, inheritable_attribute, inherited_attribute_value)
                break

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ LOCALIZATION
        # └─────────────────────────────────────────────────────────────────────────────

        # Set localized from attribute
        PyObMeta.localized_from = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ SUPER INIT
        # └─────────────────────────────────────────────────────────────────────────────

        # Call and return parent init method
        return super().__init__(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CALL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args, **kwargs):
        """Call Method"""

        # Get PyOb store
        store = cls.PyObMeta.store

        # Get counts by PyOb instance
        counts_by_pyob = store._counts_by_pyob

        # Get PyOb instances by key
        pyobs_by_key = store._pyobs_by_key

        # Initialize try-except block
        try:

            # Get PyOb instance
            pyob = super().__call__(*args, **kwargs)

        # Handle any exception encountered during initialization
        except Exception:

            # Clean up key index as if PyOb instance never existed
            # Ensures no keys for problematic instances are kept in the index
            store._obs_by_key = {
                k: v for k, v in pyobs_by_key.items() if v in counts_by_pyob
            }

            # Re-raise exception
            raise

            # NOTE: Exceptions can happen when setting individual attributes
            # The above except block ensures that PyOb initialization is atomic

        # Add PyOb instance to store
        store._counts_by_pyob[pyob] = 1

        # Return PyOb instance
        return pyob

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(cls, key):
        """Get Item Method"""

        # Apply get item to PyOb store
        return cls.PyObMeta.store[key]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INSTANCECHECK__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __instancecheck__(cls, instance):
        """Instance Check Method"""

        # Get PyOb Meta
        pyob_meta = getattr(instance.__class__, "PyObMeta", None)

        # Check if PyOb Meta is not None
        if pyob_meta is not None:

            # Get localized from
            localized_from = getattr(pyob_meta, "localized_from", None)

            # Check if localized from current class
            if localized_from and issubclass(localized_from, cls):

                # Return True
                return True

        # Return default instance check
        return super().__instancecheck__(instance)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OBS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def obs(cls):
        """Returns the PyObStore of the current PyOb class"""

        # Return PyOb store
        return cls.PyObMeta.store

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL SINGULAR
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_singular(cls):
        """Returns a singular label based on the PyObMeta definition or class name"""

        # Get singular label from PyObMeta
        label_singular = cls.PyObMeta.label_singular

        # Default singular label to derivative of class name if not defined
        label_singular = label_singular or " ".join(split_pascal(cls.__name__))

        # Strip singular label
        label_singular = label_singular.strip()

        # Return singular label
        return label_singular

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL PLURAL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_plural(cls):
        """Returns a plural label based on the PyObMeta definition or singular label"""

        # Get plural label from PyObMeta
        label_plural = cls.PyObMeta.label_plural

        # Check if plural label is null
        if not label_plural:

            # Get singular label
            label_singular = cls.label_singular

            # Check if label ends with a "y"
            if label_singular.endswith("y"):

                # Pluralize label
                label_plural = label_singular[:-1] + "ies"

            # Otherwise check if label requires "-es"
            elif label_singular.endswith(("x", "ch")):

                # Pluralize label
                label_plural = label_singular + "es"

            # Otherwise handle general case
            else:

                # Pluralize label
                label_plural = label_singular + "s"

        # Return plural label
        return label_plural
