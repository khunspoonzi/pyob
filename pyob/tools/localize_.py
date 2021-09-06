# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import pyob.ob as ob


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOCALIZE
# └─────────────────────────────────────────────────────────────────────────────────────


def localize(*classes):
    """ Localizes and returns an interable of PyOb class instances """

    # Initialize cache
    cache = {}

    # Define localize helper function
    def _localize(Class):

        # Return if class is not a PyOb subclass
        if Class is ob.Ob or not issubclass(Class, ob.Ob):
            return Class

        # Return if class in cache
        if Class in cache:
            return cache[Class]

        # Localize bases
        bases = tuple([_localize(base) for base in Class.__bases__])

        # Get and set localized class
        cache[Class] = type(Class.__name__, bases, dict(Class.__dict__))

        # Return the localized class
        return cache[Class]

    # Localize classes
    classes = [_localize(Class) for Class in classes]

    # Return localized classes
    return classes[0] if len(classes) == 1 else tuple(classes)
