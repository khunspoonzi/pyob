# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.tools import is_pyob_base
from pyob.utils import ReturnValue

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONSTANTS
# └─────────────────────────────────────────────────────────────────────────────────────

CHILD = "child"
PARENT = "parent"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB LAYER
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_layer(PyObClass, callback, layer, inclusive=False, seen=None):
    """Traverses a relative layer of a PyOb class and applies a callback to each"""

    # Return if PyOb base class
    # To avoid ever traversing from pyob.PyOb
    if is_pyob_base(PyObClass):
        return

    # Initialize seen PyOb classes
    seen = set() if seen is None else seen

    # NOTE: Only initialize a new set if seen is None
    # We may want to pass a reference to an empty set!

    # Get PyObMeta
    PyObMeta = PyObClass.PyObMeta

    # Define relatives by layer
    relatives_by_layer = {
        CHILD: PyObMeta.Children,
        PARENT: PyObMeta.Parents,
    }

    # Get relatives list
    Relatives = relatives_by_layer.get(layer, [])

    # Check if inclusive
    if inclusive:

        # Prepend PyObClass to relatives list
        # So that callback is applied to PyObClass first
        Relatives = [PyObClass] + Relatives

    # Otherwise ensure that PyObClass is in seen
    # To ensure that the callback is not applied
    else:

        # Add PyObClass to seen
        seen.add(id(PyObClass))

    # Iterate over PyOb class and relatives
    for Relative in Relatives:

        # Continue if PyOb base class
        # To avoid ever applying a callback to pyob.PyOb
        if is_pyob_base(Relative):
            continue

        # Get PyObClass ID
        class_id = id(Relative)

        # Continue if already seen
        if class_id in seen:
            continue

        # Add PyObClass ID to seen
        seen.add(class_id)

        # Apply callback function and get result
        result = callback(Relative)

        # Check if result is a ReturnValue
        if type(result) is ReturnValue:

            # Return the value of result
            return result


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB LAYERS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_layers(PyObClass, callback, layer, inclusive=False, seen=None):
    """
    Recursively traverses relative layers of a PyOb class and applies a callback to each
    """

    # Initialize seen PyOb classes
    seen = set() if seen is None else seen

    # NOTE: Only initialize a new set if seen is None
    # We may want to pass a reference to an empty set!

    # Define a callback wrapper
    def callback_wrapper(PyObClass):
        """Wraps the callback function in logic that will enable recursion"""

        # Apply callback to PyObClass
        result = callback(PyObClass)

        # Return if ReturnValue
        if type(result) is ReturnValue:
            return result

        # Traverse PyOb layers
        return traverse_pyob_layers(
            PyObClass=PyObClass,
            callback=callback,
            layer=layer,
            inclusive=False,
            seen=seen,
        )

    # Traverse PyOb layer
    return traverse_pyob_layer(
        PyObClass=PyObClass,
        callback=callback_wrapper,
        layer=layer,
        inclusive=inclusive,
        seen=seen,
    )


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB CHILDREN
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_children(*args, **kwargs):
    """Traverses the direct children of a PyOb class and applies a callback to each"""

    # Traverse PyOb child layer
    return traverse_pyob_layer(*args, **kwargs, layer=CHILD)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB DESCENDANTS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_descendants(*args, **kwargs):
    """Traverses the descendants of a PyOb class and applies a callback to each"""

    # Traverse PyOb child layers
    return traverse_pyob_layers(*args, **kwargs, layer=CHILD)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB PARENTS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_parents(*args, **kwargs):
    """Traverses the direct parents of a PyOb class and applies a callback to each"""

    # Traverse PyOb parent layer
    return traverse_pyob_layer(*args, **kwargs, layer=PARENT)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB ANCESTORS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_ancestors(*args, **kwargs):
    """Traverses the ancestors of a PyOb class and applies a callback to each"""

    # Traverse PyOb parent layers
    return traverse_pyob_layers(*args, **kwargs, layer=PARENT)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB DIRECT RELATIVES
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_direct_relatives(PyObClass, callback, *args, **kwargs):
    """Traverses the direct relatives of a PyOb class and applies a callback to each"""

    # Initialize seen PyOb classes
    seen = set()

    # Define a callback wrapper
    def callback_wrapper(PyObClass):
        """Wraps the callback function in logic that will enable recursion"""

        # Traverse PyOb descendants
        return traverse_pyob_descendants(
            PyObClass=PyObClass, callback=callback, seen=seen, inclusive=True
        )

    # Traverse PyOb ancestors
    return traverse_pyob_ancestors(
        PyObClass=PyObClass, callback=callback_wrapper, *args, **kwargs
    )
