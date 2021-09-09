# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typeguard import check_type

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import (
    DuplicateKeyError,
    InvalidKeyError,
    InvalidTypeError,
    UnicityError,
)
from pyob.tools import convert_string_to_pascal_case, is_ob


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

    def __repr__(self, _str=None):
        """ Representation Method """

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
        """ Set Attr Method """

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
        # │ ENFORCE KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get keys
        _keys = cls._keys or ()

        # Determin if key
        is_key = _keys and name in _keys

        # Check if key and is None
        if is_key and value is None:

            # Raise InvalidKeyError
            raise InvalidKeyError("A key value cannot be None")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ENFORCE TYPES
        # └─────────────────────────────────────────────────────────────────────────────

        # Determine if type checking is enabled
        enforce_types = not self._disable_type_checking

        # Check if should enforce types
        if enforce_types:

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ GET CACHED TYPE HINTS
            # └─────────────────────────────────────────────────────────────────────────

            # Get cached type hints
            _type_hints = cls._type_hints

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE TYPE HINTS
            # └─────────────────────────────────────────────────────────────────────────

            # Check if name in type hints
            if name in _type_hints:

                # Get expected type
                expected_type = _type_hints[name]

                # Initialize try-except block
                try:

                    # Check type
                    check_type(name, value, expected_type)

                # Handle TypeError
                except TypeError:

                    # Raise InvalidTypeError
                    raise InvalidTypeError(
                        f"{cls.__name__}.{name} expects a value of type "
                        f"{expected_type} but got: {value} ({type(value)})"
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
            _obs_by_key = cls._store._obs_by_key

            # Check if value in objects by key map
            if value in _obs_by_key and (other := _obs_by_key[value]) != self:

                # ┌─────────────────────────────────────────────────────────────────────
                # │ RAISE DUPLICATE KEY ERROR
                # └─────────────────────────────────────────────────────────────────────

                # Get singular label
                label_singular = cls.label_singular

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
        _unique = cls._unique or ()

        # Iterate over unique fields
        for _field in _unique:

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
            _obs_by_unique_value = cls._store._obs_by_unique_field.setdefault(
                _field, {}
            )

            # Check if unique constraint is violated
            if (
                _value in _obs_by_unique_value
                and (other := _obs_by_unique_value[_value]) != self
            ):

                # Raise UnicityError
                raise UnicityError(
                    f"A {cls.label_singular} with a(n) {_field} of {_value} "
                    f"already exists: {other}"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ RE-INDEX FIELD VALUE
            # └─────────────────────────────────────────────────────────────────────────

            if (
                is_unique_together and all([f in self.__dict__ for f in _field])
            ) or _field in self.__dict__:

                # Get previous value
                _value_previous = (
                    tuple(self.__dict__[f] for f in _field)
                    if is_unique_together
                    else self.__dict__[_field]
                )

                # Check previous value is indexed
                if _value_previous in _obs_by_unique_value:

                    # Pop previous value from index
                    _obs_by_unique_value.pop(_value_previous)

            # Index new field value
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
        """ String Method """

        # Initialize root
        root = root if root is not None else self

        # Get string field if defined otherwise the first key if any
        string_field = _str or self._str or (self._keys[0] if self._keys else None)

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
