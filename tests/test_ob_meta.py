# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import Ob
from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB META TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObMetaTestCase(PyObFixtureTestCase):
    """ Ob Meta Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST ATTRIBUTE INITIALIZATION
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_attribute_initialization(self):
        """ Ensure that user-defined attributes are initialized as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CONSTANTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define attribute constants
        KEY_1 = "key_1"
        KEY_2 = "key_2"
        UNIQUE_1 = "unique_1"
        UNIQUE_2 = "unique_2"
        UNIQUE_3 = "unique_3"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Ob):

            # Define keys
            _keys = (KEY_1, KEY_2)

            # Define unique fields
            _unique = (UNIQUE_1, (UNIQUE_2, UNIQUE_3))

        # Assert that keys are converted to tuple
        self.assertEqual(A._keys, (KEY_1, KEY_2))

        # Assert that unique fields are converted to tuples
        self.assertEqual(A._unique, (UNIQUE_1, (UNIQUE_2, UNIQUE_3)))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(Ob):

            # Define keys
            _keys = [KEY_1, KEY_2]

            # Define unique fields
            _unique = [UNIQUE_1, [UNIQUE_2, UNIQUE_3]]

        # Assert that keys are converted to tuple
        self.assertEqual(B._keys, (KEY_1, KEY_2))

        # Assert that unique fields are converted to tuples
        self.assertEqual(B._unique, (UNIQUE_1, (UNIQUE_2, UNIQUE_3)))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ C
        # └─────────────────────────────────────────────────────────────────────────────

        class C(Ob):

            # Define keys
            _keys = {KEY_1, KEY_2}

            # Define unique fields
            _unique = (UNIQUE_1, {UNIQUE_2, UNIQUE_3})

        # Assert that keys are converted to tuple
        self.assertTrue(
            type(C._keys) is tuple
            and len(C._keys) == 2
            and all([k in C._keys for k in (KEY_1, KEY_2)])
        )

        # Assert that unique fields are converted to tuples
        self.assertTrue(
            len(C._unique) == 2
            and C._unique[0] == UNIQUE_1
            and all([u in C._unique[1] for u in (UNIQUE_2, UNIQUE_3)])
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ D
        # └─────────────────────────────────────────────────────────────────────────────

        class D(Ob):

            # Define keys
            _keys = KEY_1

            # Define unique fields
            _unique = UNIQUE_1

        # Assert that keys are converted to tuple
        self.assertEqual(D._keys, (KEY_1,))

        # Assert that unique fields are converted to tuples
        self.assertEqual(D._unique, (UNIQUE_1,))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST STORE INHERITANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_store_inheritance(self):
        """ Ensure that object store inheritance behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent(Ob):
            """ A parent class """

            def __init__(self, id):
                """ Init Method """

                # Set ID
                self.id = id

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class Child(Parent):
            """ A child class """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INITIAL STORE VALUES
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that parent store is initialized and empty
        self.assertIsObStore(Parent._store, 0)

        # Assert that child store is initialized and empty
        self.assertIsObStore(Child._store, 0)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE PARENT STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Populate parent objects
        parents = Parent.Set() + [Parent(id=i) for i in range(0, 10)]

        # Assert that parents has 10 items
        self.assertIsObSet(parents, 10)

        # Assert that parent store is an ObStore of 10 items
        self.assertIsObStore(Parent._store, 10)

        # Assert that child store is still empty
        self.assertIsObStore(Child._store, 0)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE CHILD STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Populate child objects
        children = Child.Set() + [Child(id=i) for i in range(10, 30)]

        # Assert that children has 20 items
        self.assertIsObSet(children, 20)

        # Assert that child store is an ObStore of 20 items
        self.assertIsObStore(Child._store, 20)

        # Assert that parent store still has 10 items
        self.assertIsObStore(Parent._store, 10)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
