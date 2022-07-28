# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.main.tools import get_pyob_string_field, localize_pyob_class
from pyob.main.tools.validate import validate_and_index_pyob_attr
from pyob.meta import Metaclass
from pyob.tools import is_pyob_instance
from pyob.tools.object import hexify
from pyob.tools.string import pascalize


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB
# └─────────────────────────────────────────────────────────────────────────────────────


class PyOb(metaclass=Metaclass):
    """A base class for PyOb classes"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOCALIZED
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def Localized(cls, include=None):
        """Returns a localized version of the PyOb class with an empty object store"""

        # Return localized PyOb classes
        return localize_pyob_class(cls, *(include or []))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL SINGULAR
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_singular(self):
        """Returns the singular label of the instance's PyOb class"""

        # Return singular label
        return self.__class__.label_singular

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL PLURAL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_plural(self):
        """Returns the plural label of the instance's PyOb class"""

        # Return plural label
        return self.__class__.label_plural

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self):
        """Representation Method"""

        # Initialize representation to singular label
        representation = self.label_singular

        # Convert representation to Pascal case
        representation = pascalize(representation)

        # Add angle brackets to representation
        representation = f"<{representation}: {self.__str__()}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __setattr__(self, name, value):
        """Set Attr Method"""

        # Validate and index PyOb instance attribute
        validate_and_index_pyob_attr(pyob=self, name=name, value=value)

        # Call parent __setattr__ method
        super().__setattr__(name, value)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self, root=None):
        """String Method"""

        # Initialize root
        # Used to avoid cases of infinite recursion
        root = root if root is not None else self

        # Get the string field of the PyOb instance
        string_field = get_pyob_string_field(self)

        # Get string value from string field
        string_value = string_field and getattr(self, string_field, None)

        # Check if the string value is another PyOb instance
        # Analagous to the field of of a PyOb instance being a "foreign key" to another
        if is_pyob_instance(string_value):

            # Check if the associated PyOb instance isn't root and has a string field
            # If is the root then we are likely going around in circles and must break
            # If the associate PyOb instance doesn't have a string field, ignore it
            if string_value != root and get_pyob_string_field(string_value):

                # Evaluate the string value of the associated PyOb instance
                # We pass the root here for tracking to avoid infinite recursion
                string_value = string_value.__str__(root=root)

            # Otherwise handle case of no meaningful string value
            else:

                # Set string value to None
                # We avoid setting string value to hex of an associated PyOb instance
                # as this would be incredibly confusing
                string_value = None

        # Ensure that the string value defaults to the hex of the root if null
        string_value = string_value or hexify(root)

        # Ensure that the string value is a string
        string_value = str(string_value)

        # Return the string value
        return string_value

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyObMeta Class"""
