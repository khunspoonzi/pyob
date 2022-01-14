# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import (
    InvalidObjectError,
    NonExistentKeyError,
    UnrelatedObjectsError,
)
from pyob.tools import (
    filter_by_key,
    filter_by_keys,
    is_iterable,
    is_pyob,
    is_pyob_set,
)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB SET DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObSetDunderMixin:
    """A mixin class for PyOb object set dunder methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ADD__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __add__(self, others):
        """Add Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OBJECT SET
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize new object set
        new = self.New()

        # Get PyOb class
        PyObClass = new._PyObClass

        # Get object store
        store = PyObClass.PyObMeta.store

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ADD OTHER TO CURRENT
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize key cache
        key_cache = {}

        # Copy current PyOb set
        new._pyob_dict = {k: v for k, v in self._pyob_dict.items()}

        # Ensure other object group is iterable
        others = others if is_iterable(others) else [others]

        # Iterate over PyObs in other
        for other in others:

            # Continue if PyOb is None
            if other is None:
                continue

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ GET BY KEY
            # └─────────────────────────────────────────────────────────────────────────

            # Get PyOb class
            OtherPyObClass = other.__class__

            # Check if object class does not match object set
            if OtherPyObClass is not PyObClass:

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
                        pyob_dict=store._pyob_dict,
                        keys=PyObClass.PyObMeta.keys,
                        value=other,
                        ob_label_plural=PyObClass.label_plural,
                    )

                    # Check if there are any filtered objects
                    if filtered:

                        # Update object and key cache
                        other = key_cache[other] = filtered[0]

                # Set object class
                OtherPyObClass = other.__class__

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE PYOB OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Check if not PyOb object
            if not is_pyob(other):

                # Raise InvalidObjectError
                raise InvalidObjectError(
                    "Only pyob.Ob objects can be added to a pyob.ObSet, "
                    f"got {other} ({type(other)})"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ CHECK OBJECT CLASS
            # └─────────────────────────────────────────────────────────────────────────

            # Check if object class is None
            if PyObClass is None:

                # Set object set object class
                PyObClass = new._PyObClass = OtherPyObClass

            # Otherwise, check if other is not a subclass of current PyOb class
            elif not issubclass(OtherPyObClass, PyObClass):

                # Raise UnrelatedObjectsError
                raise UnrelatedObjectsError(
                    f"Cannot add {OtherPyObClass.__name__} instance to {self.name} "
                    f"unless {OtherPyObClass.__name__} inherits from "
                    f"{PyObClass.__name__}"
                )

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ ENFORCE KEY UNICITY
            # └─────────────────────────────────────────────────────────────────────────

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ UPDATE STORE
            # └─────────────────────────────────────────────────────────────────────────

            if other not in store._pyob_dict:
                store._pyob_dict[other] = 1

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ APPEND OBJECT
            # └─────────────────────────────────────────────────────────────────────────

            # Append object to objects
            new._pyob_dict[other] = (
                new._pyob_dict[other] + 1 if other in new._pyob_dict else 1
            )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RETURN NEW OBJECT SET
        # └─────────────────────────────────────────────────────────────────────────────

        # Return new object set
        return new

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __AND__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __and__(self, other):
        """And Method"""

        # Ensure other is iterable
        other = other if is_iterable(other) else [other]

        # Extract PyObs from others
        other_pyobs = [o for o in other if is_pyob(o)]

        # Extract potential keys from others
        other_keys = [o for o in other if o not in other_pyobs]

        # Resolve potential keys
        other_keys = filter_by_keys(
            pyob_dict=self._pyob_dict,
            keys=self._PyObClass.PyObMeta.keys,
            values=other_keys,
            ob_label_plural=self.ob_label_plural,
        )

        # Combine resolved objects
        other_pyobs = other_pyobs + other_keys

        # Return the new object set
        return self.New() + (set(self._pyob_dict) & set(other_pyobs))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __BOOL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __bool__(self):
        """Bool Method"""

        # Return whether object count is greater than zero
        return len(self._pyob_dict) > 0

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CONTAINS__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __contains__(self, item):
        """Contains Method"""

        # Return whether item or key in objects
        return (item in self._pyob_dict) or len(
            filter_by_key(
                pyob_dict=self._pyob_dict,
                keys=self._PyObClass.PyObMeta.keys,
                value=item,
                ob_label_plural=self.ob_label_plural,
            )
        ) > 0

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __EQ__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __eq__(self, other):
        """Eq Method"""

        # Return False if other is not a PyOb set
        if not is_pyob_set(other):
            return False

        # Return True if the PyObs of both PyOb sets match
        return self._pyob_dict == other._pyob_dict

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getattr__(self, name):
        """Get Attr Method"""

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
        """Get Item Method"""

        # Get PyObs as list
        pyobs = list(self)

        # Check if key is a slice
        if isinstance(key, slice):

            # Return a new sliced object set
            return self.New() + pyobs[key]

        # Return indexed object
        return pyobs[key]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self):
        """Iterate Method"""

        # Iterate over objects in object set
        for pyob, count in self._pyob_dict.items():

            # Iterate over object count
            for _ in range(count):

                # Yield object
                yield pyob

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self):
        """Length Method"""

        # Return length of PyOb dict
        return sum(self._pyob_dict.values())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __OR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __or__(self, other):
        """Or Method"""

        # Ensure other is iterable
        other_pyobs = other if is_iterable(other) else [other]

        # Return the new PyOb set
        return self.New() + (set(self._pyob_dict) | set(other_pyobs))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __POW__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __pow__(self, other):
        """Pow Method"""

        # Apply rshift method
        return self.__rshift__(other)

        # NOTE: Pow takes higher precedence than rshift in order of operations

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self):
        """Representation Method"""

        # Define threshold
        threshold = 20

        # Get PyOb count
        pyob_count = len(self)

        # Initialize representation as object set name
        representation = self.name

        # Add count to representation
        representation += f": {pyob_count}"

        # Get the first 20 objects
        pyobs = list(self)[:threshold]

        # Stringify PyObs according to PyOb set class string field
        pyobs = [
            pyob.__repr__(display=self._PyObClass.PyObMeta.display) for pyob in pyobs
        ]

        # Check if there are more than n objects total
        if pyob_count > threshold:

            # Add truncation message to objects list
            pyobs.append("...(remaining elements truncated)... ")

        # Add objects to representation
        representation = f"{representation} {'[' + ', '.join(pyobs) + ']'}"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __RSHIFT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __rshift__(self, other):
        """Rshift Method"""

        # Get by key
        return self.key(other)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SUB__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __sub__(self, other):
        """Sub Method"""

        # Ensure other is iterable
        other = other if is_iterable(other) else [other]

        # Return PyOb set
        return self.New() + (set(self._pyob_dict) - set(other))
