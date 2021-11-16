# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE METHOD MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreMethodMixin:
    """A mixin class for PyOb object store methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, *args, **kwargs):
        """Returns the PyOb object associated with a key from the PyOb object store"""

        # Iterate over child stores
        for ob_store in self._children:

            # Get object by key or default to None
            ob = ob_store.key(*args, **{**kwargs, "default": None})

            # Return object if found
            if ob is not None:
                return ob

        # Return parent key method assuming object store
        return super().key(*args, **kwargs)
