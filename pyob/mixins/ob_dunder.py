# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typeguard import check_type
from typing import get_type_hints

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import (
    DuplicateKeyError,
    InvalidKeyError,
    InvalidTypeError,
    UnicityError,
)
from pyob.tools import is_ob


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObDunderMixin:
    """ A mixin class for PyOb object dunder methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ADD__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __add__(self, other):
        """ Add Method """

        # Return an object set containing the two objects
        return self.Set() + self + other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self):
        """ Representation Method """

        # Initialize representation
        representation = self.label_singular

        # Add angle brackets to representation
        representation = f"<{representation}: {str(self)}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __setattr__(self, name, value):
        """ Set Attr Method """

        # Get object class
        Class = self.__class__

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CLEAN VALUE
        # └─────────────────────────────────────────────────────────────────────────────

        # Get clean methods
        _clean = Class._clean

        # Check if name in clean methods
        if name in _clean:

            # Clean value
            value = _clean[name](self, value)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ENFORCE KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get keys
        _keys = Class._keys

        # Determin if key
        is_key = _keys and name in _keys

        # Check if key and is None
        if is_key and value is None:

            # Raise InvalidKeyError
            raise InvalidKeyError("A key value cannot be None")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ENFORCE TYPES
        # └─────────────────────────────────────────────────────────────────────────────

        # Determine if type enforcement is enabled
        enforce_types = not self._disable_type_enforcement

        # Check if should enforce types
        if enforce_types:

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ GET CACHED TYPE HINTS
            # └─────────────────────────────────────────────────────────────────────────

            # Get or initialize cached type hints
            type_hints = Class._type_hints

            # Check if cached type hints is None
            if type_hints is None:

                # Initialize type hints
                type_hints = {}

                # Update type hints by init type hints
                type_hints.update(get_type_hints(self.__init__) or {})

                # Update type hints by class-level type hints
                type_hints.update(get_type_hints(Class) or {})

                # Set class-level cached type hints
                Class._type_hints = type_hints

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE TYPE HINTS
            # └─────────────────────────────────────────────────────────────────────────

            # Check if name in type hints
            if name in type_hints:

                # Get expected type
                expected_type = type_hints[name]

                # Initialize try-except block
                try:

                    # Check type
                    check_type(name, value, expected_type)

                # Handle TypeError
                except TypeError:

                    # Get singular label
                    label_singular = Class.label_singular

                    # Raise InvalidTypeError
                    raise InvalidTypeError(
                        f"{label_singular}.{name} expects a value :: {expected_type} "
                        f"but got: {value} :: {type(value)}"
                    )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COMMIT KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Check if name is key
        if is_key:

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ CHECK KEY INDEX
            # └─────────────────────────────────────────────────────────────────────────

            # Get objects by key map
            _obs_by_key = Class._store._obs_by_key

            # Check if value in objects by key map
            if value in _obs_by_key and (other := _obs_by_key[value]) != self:

                # ┌─────────────────────────────────────────────────────────────────────
                # │ RAISE DUPLICATE KEY ERROR
                # └─────────────────────────────────────────────────────────────────────

                # Get singular label
                label_singular = Class.label_singular

                # Raise DuplicateKeyError
                raise DuplicateKeyError(
                    f"A {label_singular} with a key of {value} already exists: {other}"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ RE-INDEX KEY
            # └─────────────────────────────────────────────────────────────────────────

            # Check previous value is defined
            if name in self.__dict__:

                # Get previous value
                value_previous = self.__dict__[name]

                # Check if previous value is indexed
                if value_previous in _obs_by_key:

                    # Pop previous value from index
                    _obs_by_key.pop(value_previous)

            # Add new value index to store
            _obs_by_key[value] = self

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COMMIT UNIQUE FIELDS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get unique fields
        _unique = Class._unique

        # Iterate over unique fields
        for _field in _unique or ():

            # Determine if unique together (a tuple of fields)
            is_unique_together = type(_field) is tuple

            # Determine if is unique field
            is_unique_field = (is_unique_together and name in _field) or name == _field

            # Continue if current field is not a unique field
            if not is_unique_field:
                continue

            # Check if is unique together (a tuple of fields)
            if is_unique_together:

                # Continue if field combination is not yet defined
                if not all([(f == name or f in self.__dict__) for f in _field]):
                    continue

                # Get value
                _value = tuple(value if f == name else self.__dict__[f] for f in _field)

            # Otherwise handle case of single field
            else:

                _value = value

            # Get objects by unique value given field
            _obs_by_unique_value = Class._store._obs_by_unique_field.setdefault(
                _field, {}
            )

            # Check if unique constraint is violated
            if (
                _value in _obs_by_unique_value
                and (other := _obs_by_unique_value[_value]) != self
            ):

                # Get singular label
                label_singular = Class.label_singular

                # Raise UnicityError
                raise UnicityError(
                    f"A {label_singular} with a(n) {_field} of {_value} "
                    f"already exists: {other}"
                )

            #
            _obs_by_unique_value[_value] = self

            """
            NOTE: Objects by unique field structure looks like this:

            _obs_by_unique_field = {
                "name": {"China": ff0x14},
                ("latitude", "longitude") : {(1.1, 2.2): ff0x14}
            }

            """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RETURN PARENT SET ATTR
        # └─────────────────────────────────────────────────────────────────────────────

        # Return parent set attr method
        return super().__setattr__(name, value)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self, root=None):
        """ String Method """

        # Initialize root
        root = root if root is not None else self

        # Get string field if defined otherwise the first key if any
        string_field = self._str or (self._keys[0] if self._keys else None)

        # Set string to value of string field
        string = string_field and getattr(self, string_field, None)

        # Check if string is a PyOb object
        if is_ob(string):

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
