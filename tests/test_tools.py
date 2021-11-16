# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb
from pyob.tools import traverse_pyob_relatives


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TOOLS TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ToolsTestCase(unittest.TestCase):
    """Tools Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST TRAVERSE PYOB RELATIVES
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_traverse_pyob_relatives(self):
        """Ensures that the traverse PyOb relatives tool behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # │
        # │ Show that class relations are not double traversed
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

        class B(A):
            """A PyOb test class"""

        class C(A):
            """A PyOb test class"""

        class D(C):
            """A PyOb test class"""

        # Define classes
        classes = (A, B, C, D)

        # Iterate over inclusive
        for inclusive in (True, False):

            # Iterate over classes
            for Class in classes:

                # Initialize traversed list
                traversed = []

                # Define callback
                def callback(Class):

                    # Append class to traversed
                    traversed.append(Class)

                # Traverse PyOb relatives
                traverse_pyob_relatives(Class, callback=callback, inclusive=inclusive)

                # Get list of classes that were expected to be traversed
                traversed_expected = (
                    classes if inclusive else [c for c in classes if c is not Class]
                )

                # Assert that length of traversed list is equal to number of classes
                self.assertEqual(len(traversed), len(traversed_expected))

                # Assert that all of the expected classes were traversed
                self.assertTrue(all(c in traversed for c in traversed_expected))


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
