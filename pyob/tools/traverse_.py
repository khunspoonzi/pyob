# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.ob as ob


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB BASES
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_bases(cls, callback):
    """ Traverses the PyOb base classes of a given class and applies a callback """

    # Define traverse helper
    def traverse(cls):
        """ Traverses the PyOb bases of given PyOb class """

        # Return if class is not a PyOb class
        if not issubclass(cls, ob.Ob):
            return

        # Apply callback to current PyOb class
        callback(cls)

    # Traverse PyOb base classes
    [traverse(c) for c in (cls,) + cls.__bases__]
