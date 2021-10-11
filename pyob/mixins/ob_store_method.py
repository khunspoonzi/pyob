# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB STORE METHOD MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObStoreMethodMixin:
    """ A mixin class for PyOb object store methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self):
        """ Returns a count of PyOb objects in a PyOb object store """

        # Return the count of the object store and its children
        return super().count() + sum([_child.count() for _child in self._children])

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, *args, **kwargs):
        """ Returns the PyOb object associated with a key from the PyOb object store """

        # Iterate over child stores
        for ob_store in self._children:

            # Get object by key or default to None
            ob = ob_store.key(*args, **kwargs, default=None)

            # Return object if found
            if ob is not None:
                return ob

        # Return parent key method assuming object store
        return super().key(*args, **kwargs)
