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
# │ OB LABEL TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObLabelTestCase(PyObTestCase):
    """Ob Label Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT LABELS CORRECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertLabelsCorrect(self, Class, expected_singular, expected_plural):
        """Asserts that all labels in a class are equal to their expected values"""

        # Create an instance
        instance = Class()

        # Assert that the singular labels are correct
        self.assertAllEqual(
            expected_singular,
            instance.label_singular,
            Class.label_singular,
            Class.Set().ob_label_singular,
        )

        # Assert that the plural labels are correct
        self.assertAllEqual(
            expected_plural,
            instance.label_plural,
            Class.PyObMeta.label_plural,
            Class.Set().ob_label_plural,
        )

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

        # Define nation labels
        nation_label_singular = "Nation"
        nation_label_plural = nation_label_singular + "s"

        # Assert labels are correct
        self.assertLabelsCorrect(Nation, nation_label_singular, nation_label_plural)

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

        # Assert labels are correct
        self.assertLabelsCorrect(
            Nation_, Nation_.PyObMeta.label_singular, Nation_.PyObMeta.label_plural
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LABEL NATIONALITY
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_label_nationality(self):
        """Ensures that label variants of an Ob class and instance are correct"""

        class Nationality(PyOb):
            """Nationality with no labels"""

        # Define labels
        label_singular = "Nationality"
        label_plural = "Nationalities"

        # Assert labels are correct
        self.assertLabelsCorrect(Nationality, label_singular, label_plural)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LABEL API RESPONSE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_label_api_response(self):
        """Ensures that label variants of an Ob class and instance are correct"""

        class APIResponse(PyOb):
            """API Response with no labels"""

        # Define labels
        label_singular = "API Response"
        label_plural = label_singular + "s"

        # Assert labels are correct
        self.assertLabelsCorrect(APIResponse, label_singular, label_plural)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LABEL BOX
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_label_box(self):
        """Ensures that label variants of an Ob class and instance are correct"""

        class Box(PyOb):
            """Research with no labels"""

        # Define labels
        label_singular = "Box"
        label_plural = label_singular + "es"

        # Assert labels are correct
        self.assertLabelsCorrect(Box, label_singular, label_plural)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LABEL RESEARCH
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_label_research(self):
        """Ensures that label variants of an Ob class and instance are correct"""

        class Research(PyOb):
            """Research with no labels"""

        # Define labels
        label_singular = "Research"
        label_plural = label_singular + "es"

        # Assert labels are correct
        self.assertLabelsCorrect(Research, label_singular, label_plural)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
