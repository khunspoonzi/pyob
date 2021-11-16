# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import inspect

from typing import get_type_hints

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.pyob_store import PyObStore

from pyob.mixins import PyObMetaLabelMixin
from pyob.tools import is_iterable, remove_duplicates


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB META
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObMeta(type, PyObMetaLabelMixin):
    """A metaclass for the Ob base class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(cls, *args, **kwargs):
        """Init Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize parents
        parents = []

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize store
        cls._store = PyObStore(_Ob=cls)

        # Iterate over bases
        for base in cls.__bases__:

            # Get store
            _store_parent = getattr(base, "_store", None)

            # Continue if store is not a PyOb object store
            if not isinstance(_store_parent, PyObStore):
                continue

            # Add parent to child store
            cls._store._parents.append(_store_parent)

            # Add child to parent store
            _store_parent._children.append(cls._store)

            # Add parent to parents
            parents.append(_store_parent._Ob)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ KEYS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get keys
        _keys = cls._keys or ()

        # Handle case of string value as keys
        _keys = _keys and ((_keys,) if type(_keys) is str else tuple(_keys))

        # Merge with parent keys
        _keys = sum([p._keys for p in parents] + [_keys], ())

        # Ensure that keys definition is a unique tuple
        cls._keys = remove_duplicates(_keys)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ UNIQUE FIELDS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get unique fields
        _unique = cls._unique or ()

        # Handle if unique fields is a single string
        _unique = (_unique,) if type(_unique) is str else _unique

        # Ensure that unique together fields are tuples
        _unique = tuple(tuple(f) if is_iterable(f) else f for f in _unique)

        # Merge with parent unique fields
        _unique = sum([p._unique for p in parents] + [_unique], ())

        # Ensure that unique definition is a unique tuple
        cls._unique = remove_duplicates(_unique, recursive=True)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PREPOST HOOKS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get all methods
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)

        # Define pre- and post- constants
        _PRE_ = "_pre_"
        _POST_ = "_post_"

        # Define get hook cache helper
        def get_prepost(hook):
            return {k.replace(hook, "", 1): v for k, v in methods if k.startswith(hook)}

        # Initialize pre-setter cache
        cls._pre = get_prepost(_PRE_)

        # Initialize post-setter cache
        cls._post = get_prepost(_POST_)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ TYPE HINTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize type hints
        _type_hints = {}

        # Update type hints by init type hints
        _type_hints.update(get_type_hints(cls.__init__) or {})

        # Update type hints by class-level type hints
        _type_hints.update(get_type_hints(cls) or {})

        # Set type hints
        cls._type_hints = _type_hints

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ LOCALIZATION
        # └─────────────────────────────────────────────────────────────────────────────

        # Set localized from attribute
        cls._localized_from = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        # Call and return parent init method
        return super().__init__(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CALL
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args, **kwargs):
        """Call Method"""

        # Get object store
        _store = cls._store

        # Get store objects
        _store_obs = _store._obs

        # Initialize try-except block
        try:
            # Get instance
            instance = super().__call__(*args, **kwargs)

        # Handle any exception encountered during initialization
        except Exception:

            # Clean up key index as if instance never existed
            _store._obs_by_key = {
                key: ob for key, ob in _store._obs_by_key.items() if ob in _store_obs
            }

            # Iterate over objects by unique field
            for _field in _store._obs_by_unique_field:

                # Clean up unique value index as if instance never created
                _store._obs_by_unique_field[_field] = {
                    val: ob
                    for val, ob in _store._obs_by_unique_field[_field].items()
                    if ob in _store_obs
                }

            # Re-raise exception
            raise

            # NOTE: Exceptions can happen when setting individual attributes
            # The above except block ensures that object initialization is atomic

        # Add instance to store
        cls._store._obs[instance] = 1

        # Return instance
        return instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getattr__(cls, name):
        """Get Attr Method"""

        # Attempt to return PyOb object by key
        return cls._store.__getattr__(name)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INSTANCECHECK__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __instancecheck__(cls, instance):
        """Instance Check Method"""

        # Get localized from
        _localized_from = getattr(instance.__class__, "_localized_from", None)

        # Check if localized from current class
        if _localized_from and issubclass(_localized_from, cls):

            # Return True
            return True

        # Return default instance check
        return super().__instancecheck__(instance)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __POW__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __pow__(cls, other):
        """Pow Method"""

        # Return rshift of object store
        return cls._store >> other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __RSHIFT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __rshift__(cls, other):
        """Rshift Method"""

        # Return rshift of object store
        return cls._store >> other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OBS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def obs(cls):
        """Returns the PyOb object class's object store"""

        # Return object store
        return cls._store
