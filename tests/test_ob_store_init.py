# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb
from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET INIT TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSetInitTestCase(PyObFixtureTestCase):
    """Ob Set Init Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_class_attributes(self):
        """Ensures that class attributes are initialized as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OB
        # └─────────────────────────────────────────────────────────────────────────────

        # Get store
        _store = PyOb.obs

        # Assert that objects by key and objects by unique field are an empty dict
        self.assertAllEqual(_store._obs_by_key, _store._obs_by_unique_field, {})

        # Assert that the pyob.Ob store is initialized with no parents
        self.assertAllEqual(_store._parents, [])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

        # Get store
        _store = A.obs

        # Assert that parent store is pyob.Ob store
        self.assertEqual(_store._parents, [PyOb.obs])

        # Assert that the store has no children
        self.assertEqual(_store._children, [])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(A):
            """A PyOb test class"""

        # Get store
        _store = B.obs

        # Assert that parent store is A's store
        self.assertEqual(_store._parents, [A.obs])

        # Assert that the store has no children
        self.assertEqual(_store._children, [])

        # Assert that A's child store is now B's store
        self.assertEqual(A.obs._children, [B.obs])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OB
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that the pyob.Ob store continues to have no parents
        self.assertAllEqual(PyOb.obs._parents, [])


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
