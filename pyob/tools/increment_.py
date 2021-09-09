# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.tools.traverse_ import traverse_pyob_bases

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INCREMENT STORE
# └─────────────────────────────────────────────────────────────────────────────────────


def increment_store(cls, instance):
    """ Increments the object store of a PyOb class and its bases """

    # Define callback
    def callback(cls):

        # Increment the store
        cls._store._obs[instance] = 1

    # Increment current and base stores
    traverse_pyob_bases(cls, callback)
