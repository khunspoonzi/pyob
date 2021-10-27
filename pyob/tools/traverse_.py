# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB RELATIVES
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_relatives(
    Class,
    callback,
    inclusive=False,
    ancestors=True,
    descendents=True,
    unique=True,
    seen=None,
):
    """ Traverses a PyOb class's relatives and applies a callback to each """

    # Return if we hit ob.Ob
    if not Class._store._parents:
        return

    # Initialize seen
    seen = unique and (seen or {id(Class)})

    # Check if inclusive
    if inclusive:

        # Apply callback to class
        callback(Class)

    # Get store
    _store = Class._store

    # Iterate over relative types
    for (stores, should_traverse) in (
        (_store._parents, ancestors),
        (_store._children, descendents),
    ):

        # Continue of not should traverse
        if not should_traverse:
            continue

        # Iterate over stores
        for store in stores:

            # Get class
            Class = store._Ob

            # Get class ID
            class_id = id(Class)

            # Continue if unique and seen
            if unique and class_id in seen:
                continue

            # Add class ID to seen
            unique and seen.add(class_id)

            # Traverse PyOb ancestors
            traverse_pyob_relatives(
                Class,
                callback=callback,
                inclusive=True,
                ancestors=ancestors,
                descendents=descendents,
                unique=unique,
                seen=seen,
            )


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRAVERSE PYOB ANCESTORS
# └─────────────────────────────────────────────────────────────────────────────────────


def traverse_pyob_ancestors(Class, callback, inclusive=False):
    """ Traverses a PyOb class's ancestors and applies a callback to each """

    # Traverse PyOb ances
    traverse_pyob_relatives(
        Class=Class, callback=callback, inclusive=inclusive, ancestors=True
    )
