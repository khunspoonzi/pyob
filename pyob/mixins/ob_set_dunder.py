# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import InvalidObjectError, MixedObjectsError
from pyob.tools import (
    convert_obs_dict_to_list,
    filter_by_key,
    filter_by_keys,
    is_iterable,
    is_ob,
)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSetDunderMixin:
    """ A mixin class for PyOb object set dunder methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ADD__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __add__(self, other):
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
        other = other if is_iterable(other) else [other]

        # Iterate over objects in other
        for ob in other:

            # Continue if object is None
            if ob is None:
                continue

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ GET BY KEY
            # └─────────────────────────────────────────────────────────────────────────

            # Get object class
            ob_Ob = ob.__class__

            # Check if object class does not match object set
            if ob_Ob is not _Ob:

                # ┌─────────────────────────────────────────────────────────────────────
                # │ CACHE
                # └─────────────────────────────────────────────────────────────────────

                # Check if object is in key cache
                if ob in key_cache:

                    # Get object from key cache
                    ob = key_cache[ob]

                # ┌─────────────────────────────────────────────────────────────────────
                # │ STORE
                # └─────────────────────────────────────────────────────────────────────

                # Otherwise get from store
                else:

                    # Try to use object as a key
                    filtered = filter_by_key(
                        _store._obs, _Ob._keys, ob, ob_label_plural=_Ob.label_plural
                    )

                    # Check if there are any filtered objects
                    if filtered:

                        # Update object and key cache
                        ob = key_cache[ob] = filtered[0]

                # Set object class
                ob_Ob = ob.__class__

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE PYOB OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Check if not PyOb object
            if not is_ob(ob):

                # Raise InvalidObjectError
                raise InvalidObjectError(
                    "Only pyob.Ob objects can be added to a pyob.ObSet, "
                    f"got {ob} ({type(ob)})"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ CHECK OBJECT CLASS
            # └─────────────────────────────────────────────────────────────────────────

            # Check if object class is None
            if _Ob is None:

                # Set object set object class
                _Ob = new._Ob = ob_Ob

            # Otherwise, check if object classes conflict
            elif ob_Ob is not _Ob:

                # Raise MixedObjectsError
                raise MixedObjectsError(f"Cannot add {type(ob_Ob)} to {type(_Ob)}")

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE KEY UNICITY
            # └─────────────────────────────────────────────────────────────────────────

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ UPDATE STORE
            # └─────────────────────────────────────────────────────────────────────────

            if ob not in _store._obs:
                _store._obs[ob] = 1

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ APPEND OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Append object to objects
            new._obs[ob] = new._obs[ob] + 1 if ob in new._obs else 1

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
    # │ __GETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getattr__(self, name):
        """ Get Attr Method """

        # Initialize try-except block
        try:

            # Attempt to return PyOb object by key
            return self.key(name)

        # Handle KeyError
        except KeyError:

            # Raise an AttributeError
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, key):
        """ Get Item Method """

        # Check if key is a slice
        if isinstance(key, slice):

            # Return a new sliced object set
            return self.New() + self._obs[key]

        # Return indexed object
        return self._obs[key]

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

        # Check if there are more than n objects total
        if len(self) > len(_obs):

            # Add truncation message to objects list
            _obs.append("...(remaining elements truncated)...")

        # Add objects to representation
        representation = f"{representation} {str(_obs)}"

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
