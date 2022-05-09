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
# │ PYOB SET INIT TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObSetInitTestCase(PyObFixtureTestCase):
    """PyOb Set Init Test Case"""

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

        # Assert that PyObs by key and PyObs by unique field are an empty dict
        self.assertAllEqual(_store._obs_by_key, _store._obs_by_unique_field, {})

        # Assert that PyOb is initialized with no parents
        self.assertAllEqual(PyOb.PyObMeta.Parents, [])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

        # Assert that A has one parent: PyOb
        self.assertEqual(A.PyObMeta.Parents, [PyOb])

        # Assert that A has no children
        self.assertEqual(A.PyObMeta.Children, [])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(A):
            """A PyOb test class"""

        # Assert that B has one parent: A
        self.assertEqual(B.PyObMeta.Parents, [A])

        # Assert that A has no children
        self.assertEqual(B.PyObMeta.Children, [])

        # Assert that A now has one child: B
        self.assertEqual(A.PyObMeta.Children, [B])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OB
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that PyOb continues to have no parents
        self.assertAllEqual(PyOb.PyObMeta.Parents, [])


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
