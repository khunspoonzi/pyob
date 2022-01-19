# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb
from tests.test_cases.pyob import PyObTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB SET LABEL TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObiSetLabelTestCase(PyObTestCase):
    """PyOb Set Label Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LABEL NATION
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_label_nation(self):
        """Ensures that label variants of an Ob class and instance are correct"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ DYNAMIC LABELS
        # └─────────────────────────────────────────────────────────────────────────────

        class Nation(PyOb):
            """Nation with no labels"""

        # Create a Nation set
        nations = Nation.Set()

        # Assert label singular is correct
        self.assertEqual(nations.label_singular, "Nation Set")

        # Assert label plural is correct
        self.assertEqual(nations.label_plural, "Nation Sets")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ DEFINED LABELS
        # └─────────────────────────────────────────────────────────────────────────────

        class Nation_(PyOb):
            """Nation with labels"""

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ PYOB META
            # └─────────────────────────────────────────────────────────────────────────

            class PyObMeta:
                """PyOb Meta Class"""

                # Set labels
                label_singular = "State"
                label_plural = "States"

        # Create a Nation set
        nations = Nation_.Set()

        # Assert label singular is correct
        self.assertEqual(nations.label_singular, "State Set")

        # Assert label plural is correct
        self.assertEqual(nations.label_plural, "State Sets")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
