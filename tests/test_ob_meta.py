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
            """ A test class to ensure that PyOb attributes are initialized """

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
            """ A test class to ensure that PyOb attributes are initialized """

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
            """ A test class to ensure that PyOb attributes are initialized """

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
            """ A test class to ensure that PyOb attributes are initialized """

            # Define keys
            _keys = KEY_1

            # Define unique fields
            _unique = UNIQUE_1

        # Assert that keys are converted to tuple
        self.assertEqual(D._keys, (KEY_1,))

        # Assert that unique fields are converted to tuples
        self.assertEqual(D._unique, (UNIQUE_1,))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ E
        # └─────────────────────────────────────────────────────────────────────────────

        class E(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Set keys to None
            _keys = None

            # Set unique to None
            _unique = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ F
        # └─────────────────────────────────────────────────────────────────────────────

        class F(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Set keys to None
            _keys = ["a", "b"]

            # Set unique to None
            _unique = [["c", "d"], "e"]

            # Define a clean method for a field
            def _clean_a(self, value):
                """ Clean a Method """
                return value

        # Iterate over test classes
        for Class in (E, F):

            # Iterate over iterable PyOb attributes in class
            for value in (Class._keys, Class._unique):

                # Assert that the value is initialized to a tuple
                self.assertIs(type(value), tuple)

            # Ensure that all items in unique are a tuple or string
            self.assertTrue(all([type(i) in (str, tuple) for i in Class._unique]))

        # Assert that the clean method in F class is cached
        self.assertTrue("a" in F._clean)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ G
        # └─────────────────────────────────────────────────────────────────────────────

        class G(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Set class-level type hint
            str_int: int

            # Define init method
            def __init__(
                self,
                string: str,
                integer: int,
                boolean: bool,
                floating: float,
                str_int: str,
            ):

                # Set instance attributes
                self.string = string
                self.integer = integer
                self.boolean = boolean
                self.floating = floating
                self.str_int = str_int

        # Iterate over type-hinted fields
        for field, field_type in (
            ("string", str),
            ("integer", int),
            ("boolean", bool),
            ("floating", float),
            ("str_int", int),
        ):
            # Assert that cached type hint is correct
            self.assertEqual(G._type_hints[field], field_type)

        # Assert that the obs property points to the store
        self.assertEqual(id(G.obs), id(G._store))

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
