# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE METHOD MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreMethodMixin:
    """A mixin class for PyOb store methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, *args, **kwargs):
        """Returns the PyOb associated with a key from the PyOb store"""

        # Iterate over Children
        for Child in self._PyObClass.PyObMeta.Children:

            # Get PyOb by key or default to None
            ob = Child.PyObMeta.store.key(*args, **{**kwargs, "default": None})

            # Return PyOb if found
            if ob is not None:
                return ob

        # Return parent key method assuming PyOb store
        return super().key(*args, **kwargs)
