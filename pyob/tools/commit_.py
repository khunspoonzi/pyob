# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.tools.traverse_ import traverse_pyob_bases

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COMMIT INSTANCE
# └─────────────────────────────────────────────────────────────────────────────────────


def commit_instance(cls, instance):
    """ Commits an object instance by adding it to the child and parent stores """

    # Define callback
    def callback(cls):

        # Increment the store
        cls._store._obs[instance] = 1

    # Increment current and base stores
    traverse_pyob_bases(cls, callback)
