# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import inspect

from typing import get_type_hints

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.ob_store import ObStore

from pyob.mixins import ObMetaLabelMixin
from pyob.tools import increment_store, is_iterable, remove_duplicates


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB META
# └─────────────────────────────────────────────────────────────────────────────────────


class ObMeta(type, ObMetaLabelMixin):
    """ A metaclass for the Ob base class """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(cls, *args, **kwargs):
        """ Init Method """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize store
        cls._store = ObStore(_Ob=cls)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ KEYS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get keys
        _keys = cls._keys or ()

        # Handle case of string value as keys
        _keys = _keys and ((_keys,) if type(_keys) is str else tuple(_keys))

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

        # Ensure that unique definition is a unique tuple
        cls._unique = remove_duplicates(_unique, recursive=True)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CACHE: PRE- AND POST-SETTERS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get all methods
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)

        # Define pre- and post- constants
        _PRE_ = "_pre_"
        _POST_ = "_post_"

        # Define get hook cache helper
        def get_hook_cache(hook):
            return {k.replace(hook, "", 1): v for k, v in methods if k.startswith(hook)}

        # Initialize pre-setter cache
        cls._pre = get_hook_cache(_PRE_)

        # Initialize post-setter cache
        cls._post = get_hook_cache(_POST_)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CACHE: TYPE HINTS
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
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        # Call and return parent init method
        return super().__init__(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CALL
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args, **kwargs):
        """ Call Method """

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

        # Increment store
        increment_store(cls, instance)

        # Return instance
        return instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getattr__(cls, name):
        """ Get Attr Method """

        # Attempt to return PyOb object by key
        return cls._store.__getattr__(name)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __POW__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __pow__(cls, other):
        """ Pow Method """

        # Return rshift of object store
        return cls._store >> other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __RSHIFT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __rshift__(cls, other):
        """ Rshift Method """

        # Return rshift of object store
        return cls._store >> other

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OBS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def obs(cls):
        """ Returns the PyOb object class's object store """

        # Return object store
        return cls._store
