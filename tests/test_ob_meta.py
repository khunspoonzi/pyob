# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import localize, Ob
from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB META TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObMetaTestCase(PyObFixtureTestCase):
    """ Ob Meta Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CALL COMMIT INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_call_commit_instance(self):
        """ Ensures that instances are added to child and parent object stores """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent1Global(Ob):
            """ A parent class """

        class Parent2Global(Ob):
            """ A parent class """

        class Parent3Global(Ob):
            """ A parent class """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class ChildGlobal(Parent1Global, Parent2Global):
            """ A child class """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ LOCALIZE CLASSES
        # └─────────────────────────────────────────────────────────────────────────────

        # Localize parent and child classes
        Parent1, Parent2, Parent3, Child = localize(
            Parent1Global, Parent2Global, Parent3Global, ChildGlobal
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INITIAL STORE VALUES
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that all object stores are empty
        self.assertAllEqual(
            0,
            *[
                Class.obs.count()
                for Class in (
                    Parent1Global,
                    Parent2Global,
                    Parent3Global,
                    ChildGlobal,
                    Parent1,
                    Parent2,
                    Parent3,
                    Child,
                )
            ]
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE PARENT STORES
        # └─────────────────────────────────────────────────────────────────────────────

        # Iterate over parent classes
        for Parent in (Parent1, Parent2, Parent3):

            # Create parent instances
            parents = Parent.Set() + [Parent() for i in range(0, 10)]

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
        children = Child.Set() + [Child() for i in range(0, 5)]

        # Assert that children has 5 items
        self.assertIsObSet(children, 5)

        # Assert that child store is an ObStore of 5 items
        self.assertIsObStore(Child._store, 5)

        # Iterate over parent classes
        for Parent in (Parent1, Parent2):

            # Assert that parent object store now has 15 items
            self.assertEqual(Parent.obs.count(), 15)

            # Assert that all children are in parent object store
            self.assertTrue(all([child in Parent.obs._obs for child in children]))

        # Assert that the third parent still has 10 items
        self.assertEqual(Parent3.obs.count(), 10)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ GLOBAL CLASSES
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that the object stores of all global classes are still empty
        self.assertAllEqual(
            0,
            *[
                Class.obs.count()
                for Class in (Parent1Global, Parent2Global, Parent3Global, ChildGlobal)
            ]
        )

        # Ensure that pyob.Ob is not affected by the commit
        self.assertEqual(Ob.obs.count(), 0)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CALL ROLLBACK INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_call_rollback_instance(self):
        """ Ensures that instances are added to child and parent object stores """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent1Global(Ob):
            """ A parent class """

            # Set keys
            _keys = ("key1",)

            # Set unique fields
            _unique = ("unique1", ("unique2", "unique3"))

            # Define init method
            def __init__(self, key1, unique1, unique2, unique3):
                """ Init Method """

                # Set key1
                self.key1 = key1

                # Set unique fields
                self.unique1 = unique1
                self.unique2 = unique2
                self.unique3 = unique3

        class Parent2Global(Ob):
            """ A parent class """

            # Set keys
            _keys = ("key2",)

            # Set unique fields
            _unique = ("unique4", ("unique5", "unique6"))

            # Define init method
            def __init__(self, key2, unique4, unique5, unique6):
                """ Init Method """

                # Set key2
                self.key2 = key2

                # Set unique fields
                self.unique4 = unique4
                self.unique5 = unique5
                self.unique6 = unique6

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class ChildGlobal(Parent1Global, Parent2Global):
            """ A child class """

            # Set keys
            _keys = ("key3",)

            # Set unique fields
            _unique = ("unique7", ("unique8", "unique9"))

            # Define init method
            def __init__(
                self,
                key1,
                key2,
                key3,
                unique1,
                unique2,
                unique3,
                unique4,
                unique5,
                unique6,
                unique7,
                unique8,
                unique9,
            ):
                """ Init Method """

                # Call parent init methods
                Parent1Global.__init__(self, key1, unique1, unique2, unique3)
                Parent2Global.__init__(self, key2, unique4, unique5, unique6)

                # Set key3
                self.key3 = key3

                # Set unique fields
                self.unique7 = unique7
                self.unique8 = unique8
                self.unique9 = unique9

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ LOCALIZE CLASSES
        # └─────────────────────────────────────────────────────────────────────────────

        # Localize parent and child classes
        Parent1, Parent2, Child = localize(Parent1Global, Parent2Global, ChildGlobal)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INITIAL STORE VALUES
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that all object stores are empty
        self.assertAllEqual(
            0,
            *[
                Class.obs.count()
                for Class in (
                    Parent1Global,
                    Parent2Global,
                    ChildGlobal,
                    Parent1,
                    Parent2,
                    Child,
                )
            ]
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE CHILD CLASSES
        # └─────────────────────────────────────────────────────────────────────────────

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
    # │ TEST INIT CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_init_class_attributes(self):
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

        # Iterate over iterable types
        for itertype in (tuple, list):

            # ┌─────────────────────────────────────────────────────────────────────────
            # │ A
            # └─────────────────────────────────────────────────────────────────────────

            class A1(Ob):
                """ A test class to ensure that PyOb attributes are initialized """

                # Define keys
                _keys = itertype((KEY_1, KEY_2))

                # Define unique fields
                _unique = itertype((UNIQUE_1, itertype((UNIQUE_2, UNIQUE_3))))

            class A2(Ob):
                """ A test class to ensure that PyOb attributes are initialized """

                # Define keys
                _keys = itertype((KEY_1, KEY_2, KEY_2))

                # Define unique fields
                _unique = itertype(
                    (UNIQUE_1, UNIQUE_1, itertype((UNIQUE_2, UNIQUE_3, UNIQUE_3)))
                )

                # NOTE: Duplicate values should be removed

            # Iterate over A classes
            for A in (A1, A2):

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
            _keys = {KEY_1, KEY_2}

            # Define unique fields
            _unique = (UNIQUE_1, {UNIQUE_2, UNIQUE_3})

        # Assert that keys are converted to tuple
        self.assertTrue(
            type(B._keys) is tuple
            and len(B._keys) == 2
            and all([k in B._keys for k in (KEY_1, KEY_2)])
        )

        # Assert that unique fields are converted to tuples
        self.assertTrue(
            len(B._unique) == 2
            and B._unique[0] == UNIQUE_1
            and all([u in B._unique[1] for u in (UNIQUE_2, UNIQUE_3)])
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ C
        # └─────────────────────────────────────────────────────────────────────────────

        class C(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Define keys
            _keys = KEY_1

            # Define unique fields
            _unique = UNIQUE_1

        # Assert that keys are converted to tuple
        self.assertEqual(C._keys, (KEY_1,))

        # Assert that unique fields are converted to tuples
        self.assertEqual(C._unique, (UNIQUE_1,))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ D
        # └─────────────────────────────────────────────────────────────────────────────

        class D(Ob):
            """ A test class to ensure that PyOb attributes are initialized """

            # Set keys to None
            _keys = None

            # Set unique to None
            _unique = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ E
        # └─────────────────────────────────────────────────────────────────────────────

        class E(Ob):
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
        for Class in (D, E):

            # Iterate over iterable PyOb attributes in class
            for value in (Class._keys, Class._unique):

                # Assert that the value is initialized to a tuple
                self.assertIs(type(value), tuple)

            # Ensure that all items in unique are a tuple or string
            self.assertTrue(all([type(i) in (str, tuple) for i in Class._unique]))

        # Assert that the pre-setter method in E class is cached
        self.assertTrue("a" in E._pre)

        # Assert that the post-setter method in E class is cached
        self.assertTrue("b" in E._post)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ F
        # └─────────────────────────────────────────────────────────────────────────────

        class F(Ob):
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
            self.assertEqual(F._type_hints[field], field_type)

        # Assert that the obs property points to the store
        self.assertEqual(id(F.obs), id(F._store))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST INIT PREPOST HOOK INHERITANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_init_prepost_hook_inheritance(self):
        """ Ensures that prepost hooks are inherited as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent(Ob):
            """ Parent Class """

            # Define init method
            def __init__(self, multiplied):

                # Set multiplied
                self.multiplied = multiplied

            # Define pre hook method
            def _pre_multiplied(self, value):
                return value * 2

            # Define post hook method
            def _post_multiplied(self, value):
                return 2

        # Create new parent instance
        parent = Parent(3)

        # Assert that multiplied field is multiplied
        self.assertEqual(parent.multiplied, 6)

        # Assert that post hook returns 2
        self.assertEqual(parent._post_multiplied(None), 2)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class Child(Parent):
            """ Child Class """

            # Define pre hook method
            def _pre_multiplied(self, value):
                return value * 3

            # Define post hook method
            def _post_multiplied(self, value):
                return 3

        # Create new child instance
        child = Child(3)

        # Assert that multiplied field is multiplied
        self.assertEqual(child.multiplied, 9)

        # Assert that post hook returns 2
        self.assertEqual(child._post_multiplied(None), 3)

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


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
