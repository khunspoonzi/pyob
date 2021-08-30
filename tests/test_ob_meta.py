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

            # Define a pre-setter method for a field
            def _pre_a(self, value):
                """ Pre-setter for the a field """
                return value

            # Define a post-setter method for b field
            def _post_b(self, value):
                """ Post-setter for the a field """
                return value

        # Iterate over test classes
        for Class in (E, F):

            # Iterate over iterable PyOb attributes in class
            for value in (Class._keys, Class._unique):

                # Assert that the value is initialized to a tuple
                self.assertIs(type(value), tuple)

            # Ensure that all items in unique are a tuple or string
            self.assertTrue(all([type(i) in (str, tuple) for i in Class._unique]))

        # Assert that the pre-setter method in F class is cached
        self.assertTrue("a" in F._pre)

        # Assert that the post-setter method in F class is cached
        self.assertTrue("b" in F._post)

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
    # │ TEST GETATTR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_getattr(self):
        """ Ensures that the getattr dunder method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get Country
        Country = self.Country

        # Get countries
        countries = Country.obs

        # Get Thailand
        tha = countries.THA

        # Assert that getattr works on the Class
        self.assertEqual(Country.THA, tha)

        # Initialize assertRaises block
        with self.assertRaises(AttributeError):

            # Try to access an invalid ISO3 on Country
            Country.XXX

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        # Define constants
        _JPN = "JPN"
        THA = "THA"
        USA = "USA"

        class A(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Set JPN as a class attribute
            JPN = _JPN

            # Define keys
            _keys = ("iso3",)

            # Define init method
            def __init__(self, THA, iso3):
                """ Init Method """

                # Set instance attributes
                self.THA = THA
                self.iso3 = iso3

        # Initialize an A instance without a getattr conflict
        usa = A(THA=THA, iso3=USA)

        # Assert that JPN attribute is accessible
        self.assertEqual(A.JPN, _JPN)

        # Initialize assertRaises block
        with self.assertRaises(AttributeError):

            # Try to access non-existant THA class attribute
            A.THA

        # Assert that USA key accessor works
        self.assertEqual(A.USA, usa)

        # Initialize an A instance with an instance getattr conflict
        tha = A(THA=THA, iso3=THA)

        # Assert that the dot accessor returns instance as THA is not a class attribute
        self.assertEqual(A.THA, tha)

        # Initialize an A instance with a class  getattr conflict
        jpn = A(THA=THA, iso3=_JPN)

        # Assert that the class attribute takes precedence in the dot accessor
        self.assertEqual(A.JPN, _JPN)

        # Assert that the rshift and pow key accessors still point to instance
        self.assertEqual(A >> _JPN, jpn)
        self.assertEqual(A ** _JPN, jpn)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST POW
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_pow(self):
        """ Ensures that the pow dunder method behaves as expected """

        # Get Country
        Country = self.Country

        # Get countries
        countries = Country.obs

        # Get Thailand
        tha = countries.THA

        # Assert that pow works on CountryStore
        self.assertEqual(Country.obs ** "THA", tha)

        # Assert that pow works on the class as well
        self.assertEqual(Country ** "THA", tha)

        # Get United States
        usa = countries.USA

        # Assert that pow operator takes precedence in order of operations
        self.assertEqual(Country.obs ** "THA" + usa, tha + usa)

        # Assert that this is the case on the class as well
        self.assertEqual(Country ** "THA" + usa, tha + usa)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST RSHIFT
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_rshift(self):
        """ Ensures that the rshift dunder method behaves as expected """

        # Get Country
        Country = self.Country

        # Get countries
        countries = Country.obs

        # Get Thailand
        tha = countries.THA

        # Assert that rshift works on CountryStore
        self.assertEqual(Country.obs >> "THA", tha)

        # Assert that rshift works on the class as well
        self.assertEqual(Country >> "THA", tha)

        # Get United States
        usa = countries.USA

        # Initialize AssertRaises block
        with self.assertRaises(TypeError):

            # Ensure that the rshift operator takes a lower precedence
            Country.obs >> "THA" + usa

        # Initialize AssertRaises block
        with self.assertRaises(TypeError):

            # Ensure that precedence is the same on the class
            Country >> "THA" + usa

        # Assert that low precedence can be fixed with parenthesis
        self.assertEqual((Country.obs >> "THA") + usa, tha + usa)

        # Assert that this is the case on the class as well
        self.assertEqual((Country >> "THA") + usa, tha + usa)

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
