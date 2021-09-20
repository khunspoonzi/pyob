# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import (
    InvalidObjectError,
    NonExistentKeyError,
    UnrelatedObjectsError,
)
from pyob.tools import (
    convert_obs_dict_to_list,
    filter_by_key,
    filter_by_keys,
    is_iterable,
    is_ob,
    is_ob_set,
)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSetDunderMixin:
    """ A mixin class for PyOb object set dunder methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ADD__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __add__(self, others):
        """ Add Method """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OBJECT SET
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize new object set
        new = self.New()

        # Get object class
        _Ob = new._Ob

        # Get object store
        _store = _Ob._store

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ADD OTHER TO CURRENT
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize key cache
        key_cache = {}

        # Copy current object set
        new._obs = {k: v for k, v in self._obs.items()}

        # Ensure other object group is iterable
        others = others if is_iterable(others) else [others]

        # Iterate over objects in other
        for other in others:

            # Continue if object is None
            if other is None:
                continue

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ GET BY KEY
            # └─────────────────────────────────────────────────────────────────────────

            # Get object class
            other_Ob = other.__class__

            # Check if object class does not match object set
            if other_Ob is not _Ob:

                # ┌─────────────────────────────────────────────────────────────────────
                # │ CACHE
                # └─────────────────────────────────────────────────────────────────────

                # Check if object is in key cache
                if other in key_cache:

                    # Get object from key cache
                    other = key_cache[other]

                # ┌─────────────────────────────────────────────────────────────────────
                # │ STORE
                # └─────────────────────────────────────────────────────────────────────

                # Otherwise get from store
                else:

                    # Try to use object as a key
                    filtered = filter_by_key(
                        _store._obs, _Ob._keys, other, ob_label_plural=_Ob.label_plural
                    )

                    # Check if there are any filtered objects
                    if filtered:

                        # Update object and key cache
                        other = key_cache[other] = filtered[0]

                # Set object class
                other_Ob = other.__class__

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE PYOB OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Check if not PyOb object
            if not is_ob(other):

                # Raise InvalidObjectError
                raise InvalidObjectError(
                    "Only pyob.Ob objects can be added to a pyob.ObSet, "
                    f"got {other} ({type(other)})"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ CHECK OBJECT CLASS
            # └─────────────────────────────────────────────────────────────────────────

            # Check if object class is None
            if _Ob is None:

                # Set object set object class
                _Ob = new._Ob = other_Ob

            # Otherwise, check if other is not a subclass of current PyOb class
            elif not issubclass(other_Ob, _Ob):

                # Raise UnrelatedObjectsError
                raise UnrelatedObjectsError(
                    f"Cannot add {other_Ob.__name__} instance to {self.name} unless "
                    f"{other_Ob.__name__} inherits from {_Ob.__name__}"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE KEY UNICITY
            # └─────────────────────────────────────────────────────────────────────────

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ UPDATE STORE
            # └─────────────────────────────────────────────────────────────────────────

            if other not in _store._obs:
                _store._obs[other] = 1

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ APPEND OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Append object to objects
            new._obs[other] = new._obs[other] + 1 if other in new._obs else 1

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RETURN NEW OBJECT SET
        # └─────────────────────────────────────────────────────────────────────────────

        # Return new object set
        return new

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __AND__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __and__(self, other):
        """ And Method """

        # Ensure other is iterable
        other = other if is_iterable(other) else [other]

        # Extract PyOb objects from others
        other_obs = [o for o in other if is_ob(o)]

        # Extract potential keys from others
        other_keys = [o for o in other if o not in other_obs]

        # Resolve potential keys
        other_keys = filter_by_keys(
            self._obs, self._keys, other_keys, ob_label_plural=self.ob_label_plural
        )

        # Combine resolved objects
        other_obs = other_obs + other_keys

        # Return the new object set
        return self.New() + (set(self._obs) & set(other_obs))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __BOOL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __bool__(self):
        """ Bool Method """

        # Return whether object count is greater than zero
        return len(self._obs) > 0

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CONTAINS__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __contains__(self, item):
        """ Contains Method """

        # Return whether item or key in objects
        return (item in self._obs) or len(
            filter_by_key(
                self._obs, self._keys, item, ob_label_plural=self.ob_label_plural
            )
        ) > 0

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __EQ__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __eq__(self, other):
        """ Eq Method """

        # Return False if other is not an object set
        if not is_ob_set(other):
            return False

        # Return True if the objects of both object sets match
        return self._obs == other._obs

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getattr__(self, name):
        """ Get Attr Method """

        # Initialize try-except block
        try:

            # Attempt to return PyOb object by key
            return self.key(name)

        # Handle NonExistentKeyError
        except NonExistentKeyError:

            # Raise an AttributeError
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, key):
        """ Get Item Method """

        # Get objects as list
        _obs = convert_obs_dict_to_list(self._obs)

        # Check if key is a slice
        if isinstance(key, slice):

            # Return a new sliced object set
            return self.New() + _obs[key]

        # Return indexed object
        return _obs[key]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self):
        """ Iterate Method """

        # Return objects
        return iter(self._obs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self):
        """ Length Method """

        # Return length of objects
        return len(self._obs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __OR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __or__(self, other):
        """ Or Method """

        # Ensure other is iterable
        other_obs = other if is_iterable(other) else [other]

        # Return the new object set
        return self.New() + (set(self._obs) | set(other_obs))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __POW__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __pow__(self, other):
        """ Pow Method """

        # Apply rshift method
        return self.__rshift__(other)

        # NOTE: Pow takes higher precedence than rshift in order of operations

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self):
        """ Representation Method """

        # Initialize representation as object set name
        representation = self.name

        # Add count to representation
        representation += f": {self.count()}"

        # Get the first 20 objects
        _obs = convert_obs_dict_to_list(self._obs)[:20]

        # Stringify objects according to object set class string field
        _obs = [_ob.__repr__(_str=self._Ob._str) for _ob in _obs]

        # Check if there are more than n objects total
        if len(self) > len(_obs):

            # Add truncation message to objects list
            _obs.append("...(remaining elements truncated)... ")

        # Add objects to representation
        representation = f"{representation} {'[' + ', '.join(_obs) + ']'}"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __RSHIFT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __rshift__(self, other):
        """ Rshift Method """

        # Get by key
        return self.key(other)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SUB__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __sub__(self, other):
        """ Sub Method """

        # Ensure other is iterable
        other = other if is_iterable(other) else [other]

        # Return object set
        return self.New() + (set(self._obs) - set(other))
