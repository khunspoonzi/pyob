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
# │ PYOB STORE METHOD TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreMethodTestCase(PyObFixtureTestCase):
    """PyOb Store Method Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_count(self):
        """Ensures that the count method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get Country
        Country = self.Country

        # Get country count
        country_count = Country.obs.count()

        # Assert that count method invokes __len__ dunder
        self.assertAllEqual(country_count, len(Country.obs), Country.obs.__len__(), 250)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A generic test class"""

        class B(A):
            """A generic test class"""

        class C(B):
            """A generic test class"""

        class D(B):
            """A generic test class"""

        # Define instance counts
        instance_counts = {A: 1, B: 3, C: 5, D: 7}

        # Iterate over class instance counts
        for Class, count in instance_counts.items():

            # Assert that current count is 0
            self.assertAllEqual(
                Class.obs.count(), len(Class.obs), Class.obs.__len__(), 0
            )

            # Initialize instances
            [Class() for _ in range(count)]

            # Assert that count reflects created instances
            self.assertAllEqual(
                Class.obs.count(), len(Class.obs), Class.obs.__len__(), count
            )

        # Iterate over classes
        for Class, *rest in ((A, B, C, D), (B, C, D), (C,), (D,)):

            # Assert that the count of the parent class is cumulative
            self.assertAllEqual(
                Class.obs.count(),
                len(Class.obs),
                Class.obs.__len__(),
                instance_counts[Class] + sum(instance_counts[r] for r in rest),
            )


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
