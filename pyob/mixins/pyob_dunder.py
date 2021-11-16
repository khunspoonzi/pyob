# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.tools import (
    convert_string_to_pascal_case,
    is_pyob,
    validate_and_index_pyob_attribute_value,
)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObDunderMixin:
    """A mixin class for PyOb object dunder methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ADD__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __add__(self, other):
        """Add Method"""

        # Return an object set containing the two objects
        return self.Set() + self + other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self, _str=None):
        """Representation Method"""

        # Initialize representation
        representation = self.label_singular

        # Convert representation to Pascal case
        representation = convert_string_to_pascal_case(representation)

        # Add angle brackets to representation
        representation = f"<{representation}: {self.__str__(_str=_str)}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __setattr__(self, name, value):
        """Set Attr Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Get object class
        cls = self.__class__

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PRE-SETTER
        # └─────────────────────────────────────────────────────────────────────────────

        # Get pre-setter methods
        _pre = cls._pre or {}

        # Check if name in pre-setter methods
        if name in _pre:

            # Apply pre-setter to value
            value = _pre[name](self, value)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ VALIDATE AND INDEX ATTRIBUTE VALUE
        # └─────────────────────────────────────────────────────────────────────────────

        # Validate and index attribute value
        validate_and_index_pyob_attribute_value(cls, self, name, value)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RETURN PARENT SET ATTR
        # └─────────────────────────────────────────────────────────────────────────────

        # Call parent set attr method
        super().__setattr__(name, value)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POST-SETTER
        # └─────────────────────────────────────────────────────────────────────────────

        # Get post-setter methods
        _post = cls._post or {}

        # Check if name in post-setter methods
        if name in _post:

            # Apply post-setter to value
            value = _post[name](self, value)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self, root=None, _str=None):
        """String Method"""

        # Initialize root
        root = root if root is not None else self

        # Get string field if defined otherwise the first key if any
        string_field = _str or self._str or (self._keys[0] if self._keys else None)

        # Set string to value of string field
        string = string_field and getattr(self, string_field, None)

        # Check if string is a PyOb object
        if is_pyob(string):

            # Check if related object is not root and has a string field
            if string != root and (string._str or string._keys):

                # Evaluate the string of the related object
                # Root is passed for comparison to avoid cases of infinite recursion
                string = string.__str__(root=root)

            # Otherwise ignore the object
            else:

                # Set string to None
                # Otherwise would return the hex which would be confusing
                string = None

        # Set default to hex address if string is null
        string = string or hex(id(root))

        # Ensure string is actually a string
        string = str(string)

        # Return string
        return string
