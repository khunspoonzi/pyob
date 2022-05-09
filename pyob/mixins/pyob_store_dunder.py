# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE DUNDER MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreDunderMixin:
    """A mixin class for PyOb store dunder methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CONTAINS__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __contains__(self, item):
        """Contains Method"""

        # Return the result of contains for current and child stores
        return super().__contains__(item) or any(
            [
                Child.PyObMeta.store.__contains__(item)
                for Child in self._PyObClass.PyObMeta.Children
            ]
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self):
        """Iterate Method"""

        # Yield from current store
        yield from super().__iter__()

        # Iterate over Children
        for Child in self._PyObClass.PyObMeta.Children:

            # Yield from child store
            yield from Child.PyObMeta.store.__iter__()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self):
        """Len Method"""

        # Return the count of the PyOb store and its children
        return super().__len__() + sum(
            [len(Child.PyObMeta.store) for Child in self._PyObClass.PyObMeta.Children]
        )
