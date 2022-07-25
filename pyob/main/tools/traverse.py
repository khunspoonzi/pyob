# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.utils import ReturnValue


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB RELATIONS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_relations(
    PyObClass,
    callback,
    inclusive=False,
    ancestors=False,
    descendants=False,
    is_root=True,
    seen=None,
):
    """Traverses a PyOb class's relations and applies a callback to each"""

    # Return if we hit the PyOb base
    # Direct children of the PyOb base are not related
    if not PyObClass.PyObMeta.Parents:
        return

    # Initialize result
    result = None

    # Initialize seen
    seen = seen or {id(PyObClass)}

    # Check if inclusive
    if inclusive:

        # Apply callback to class
        result = callback(PyObClass)

    # Check if result is a ReturnValue
    if type(result) is ReturnValue:

        # Check if is root
        if is_root:

            # Extract value from result
            result = result.value

    # Otherwise continue traversal
    else:

        # Iterate over relative types
        for (Relatives, should_traverse) in (
            (PyObClass.PyObMeta.Parents, ancestors),
            (PyObClass.PyObMeta.Children, descendants),
        ):

            # Continue of not should traverse
            if not should_traverse:
                continue

            # Iterate over relatives
            for Relative in Relatives:

                # Get class ID
                class_id = id(Relative)

                # Continue seen
                if class_id in seen:
                    continue

                # Add class ID to seen
                seen.add(class_id)

                # Traverse PyOb relations
                result = traverse_pyob_relations(
                    PyObClass=Relative,
                    callback=callback,
                    inclusive=True,
                    ancestors=ancestors,
                    descendants=descendants,
                    is_root=False,
                    seen=seen,
                )

                # Check if result is a ReturnValue instance
                if type(result) is ReturnValue:

                    # Check if is root
                    if is_root:

                        # Extract value from result
                        result = result.value

                    # Break here
                    break

    # Return result
    return result


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB RELATIVES
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_relatives(PyObClass, callback, inclusive=False):
    """Traverses a PyOb class's relatives and applies a callback to each"""

    # Traverse PyOb relatives
    return traverse_pyob_relations(
        PyObClass=PyObClass,
        callback=callback,
        inclusive=inclusive,
        ancestors=True,
        descendants=True,
    )
