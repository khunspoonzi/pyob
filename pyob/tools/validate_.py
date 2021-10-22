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


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ VALIDATE PYOB ATTRIBUTE VALUE
# └─────────────────────────────────────────────────────────────────────────────────────


def validate_pyob_attribute_value(Class, instance, name, value, should_index):
    """ Validates (and indexes) the attribute value """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE KEY TYPE
    # └─────────────────────────────────────────────────────────────────────────────────

    # Get keys
    _keys = Class._keys or ()

    # Determine if key
    is_key = _keys and name in _keys

    # Check if key and is None
    if is_key and value is None:

        # Raise InvalidKeyError
        raise InvalidKeyError(
            "{cls.__name__}.{name}, a key, cannot have a value of None"
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE GENERAL TYPES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Determine if type checking is enabled
    enforce_types = not Class._disable_type_checking

    # Check if should enforce types
    if enforce_types:

        # Get cached type hints
        _type_hints = Class._type_hints

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
                    f"{Class.__name__}.{name} expects a value of type "
                    f"{expected_type} but got: {value} ({type(value)})"
                )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE KEY UNICITY
    # └─────────────────────────────────────────────────────────────────────────────────

    # Check if is key
    if is_key:

        # Get objects by key map
        _obs_by_key = Class._store._obs_by_key

        # Check if value in objects by key map
        if value in _obs_by_key:

            # Get other
            other = _obs_by_key[value]

            # Check if existing index is not the current object
            if other != instance:

                # Get singular label
                label_singular = Class.label_singular

                # Raise DuplicateKeyError
                raise DuplicateKeyError(
                    f"A {label_singular} with a key of {value} already exists: "
                    f"{other}"
                )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ VALIDATE UNIQUE FIELDS
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize
    unique_values = []

    # Get unique fields
    _unique = Class._unique or ()

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
            if not all([(f == name or f in instance.__dict__) for f in _field]):
                continue

            # Get value
            _value = tuple(value if f == name else instance.__dict__[f] for f in _field)

        # Otherwise handle case of single field
        else:

            _value = value

        # Get objects by unique value given field
        _obs_by_unique_value = Class._store._obs_by_unique_field.setdefault(_field, {})

        """
        NOTE: Objects by unique field structure looks like this:

        _obs_by_unique_field = {
            "name": {"China": ff0x14},
            ("latitude", "longitude") : {(1.1, 2.2): ff0x14}
        }

        """

        # Check if value is already indexed
        if _value in _obs_by_unique_value:

            # Get other
            other = _obs_by_unique_value[_value]

            # Check if unique constraint is violated
            if other != instance:

                # Raise UnicityError
                raise UnicityError(
                    f"A {Class.label_singular} with a(n) {_field} of {_value} "
                    f"already exists: {other}"
                )

        # Check if should index
        if should_index:

            # Append unique value to unique values
            unique_values.append(
                (_field, _value, _obs_by_unique_value, is_unique_together)
            )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INDEX VALUE
    # └─────────────────────────────────────────────────────────────────────────────────

    # Check if should index
    if should_index:

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INDEX KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Check if is key
        if is_key:

            # Get objects by key map
            _obs_by_key = Class._store._obs_by_key

            # Check previous value is defined
            if name in instance.__dict__:

                # Get previous value
                value_previous = instance.__dict__[name]

                # Check if previous value is indexed
                if value_previous in _obs_by_key:

                    # Pop previous value from index
                    _obs_by_key.pop(value_previous)

            # Add new value index to store
            _obs_by_key[value] = instance

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INDEX UNIQUE FIELDS
        # └─────────────────────────────────────────────────────────────────────────────

        for _field, _value, _obs_by_unique_value, is_unique_together in unique_values:

            if (
                is_unique_together and all([f in instance.__dict__ for f in _field])
            ) or _field in instance.__dict__:

                # Get previous value
                _value_previous = (
                    tuple(instance.__dict__[f] for f in _field)
                    if is_unique_together
                    else instance.__dict__[_field]
                )

                # Check previous value is indexed
                if _value_previous in _obs_by_unique_value:

                    # Pop previous value from index
                    _obs_by_unique_value.pop(_value_previous)

            # Index new field value
            _obs_by_unique_value[_value] = instance


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ VALIDATE AND INDEX PYOB ATTRIBUTE VALUE
# └─────────────────────────────────────────────────────────────────────────────────────


def validate_and_index_pyob_attribute_value(cls, self, name, value):
    """ Validates and indexes a PyOb instance attribute value """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TRAVERSE
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize seen cache
    seen = set()

    # Get root store ID
    root_store_id = id(cls._store)

    # Define traverse helper
    def traverse(cls):
        """ Traverses the parent and child object stores of a PyOb class """

        # Get object store
        _store = cls._store

        # Get object store ID
        _store_id = id(_store)

        # Get parent and child stores
        parents, children = _store._parents, _store._children

        # Iterate over stores
        for store in parents + children + [_store]:

            # Continue if no parent stores, i.e. is pyob.Ob
            # Otherwise we are validating against every pyob.Ob class in the runtime
            if not store._parents:
                continue

            # Get store ID
            store_id = id(store)

            # Continue if store in seen
            if store_id in seen:
                continue

            # Add store ID to seen
            seen.add(store_id)

            # Get store class
            Class = store._Ob

            # Validate (and index) value
            validate_pyob_attribute_value(
                Class=Class,
                instance=self,
                name=name,
                value=value,
                should_index=store_id == root_store_id,
            )

            # Traverse store class
            store_id != _store_id and traverse(Class)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TRAVERSE PYOB CLASSES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Traverse object stores
    traverse(cls)

    # TEST unicity
    # Be sure to ignore pyob.Ob and WRITE TEST
    # OPTIMIZE by caching seen unique fields and keys
    # TEST that the correct class is reference in store iteration (redefine cls)
    # FIX traversal so that it recurses properly
