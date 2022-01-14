# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import localize, PyOb
from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB META TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObMetaTestCase(PyObFixtureTestCase):
    """PyOb Meta Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CALL COMMIT INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_call_commit_instance(self):
        """Ensures that instances are added to child and parent object stores"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent1Global(PyOb):
            """A parent class"""

        class Parent2Global(PyOb):
            """A parent class"""

        class Parent3Global(PyOb):
            """A parent class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class ChildGlobal(Parent1Global, Parent2Global):
            """A child class"""

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
            self.assertIsObStore(Parent.PyObMeta.store, 10)

            # Assert that child store is still empty
            self.assertIsObStore(Child.PyObMeta.store, 0)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE CHILD STORE
        # └─────────────────────────────────────────────────────────────────────────────

        # Populate child objects
        children = Child.Set() + [Child() for i in range(0, 5)]

        # Assert that children has 5 items
        self.assertIsObSet(children, 5)

        # Assert that child store is an ObStore of 5 items
        self.assertIsObStore(Child.PyObMeta.store, 5)

        # Iterate over parent classes
        for Parent in (Parent1, Parent2):

            # Assert that parent object store now has 15 items
            self.assertEqual(Parent.obs.count(), 15)

            # Assert that all children are in parent object store
            self.assertTrue(all([child in Parent.obs for child in children]))

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

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CALL ROLLBACK INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_call_rollback_instance(self):
        """Ensures that instances are added to child and parent object stores"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent1Global(PyOb):
            """A parent class"""

            # Define init method
            def __init__(self, key1, unique1, unique2, unique3):
                """Init Method"""

                # Set key1
                self.key1 = key1

                # Set unique fields
                self.unique1 = unique1
                self.unique2 = unique2
                self.unique3 = unique3

            # Define PyOb Meta
            class PyObMeta:

                # Set keys
                keys = ("key1",)

                # Set unique fields
                unique = ("unique1", ("unique2", "unique3"))

        class Parent2Global(PyOb):
            """A parent class"""

            # Define init method
            def __init__(self, key2, unique4, unique5, unique6):
                """Init Method"""

                # Set key2
                self.key2 = key2

                # Set unique fields
                self.unique4 = unique4
                self.unique5 = unique5
                self.unique6 = unique6

            # Define PyOb Meta
            class PyObMeta:

                # Set keys
                keys = ("key2",)

                # Set unique fields
                unique = ("unique4", ("unique5", "unique6"))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class ChildGlobal(Parent1Global, Parent2Global):
            """A child class"""

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
                """Init Method"""

                # Call parent init methods
                Parent1Global.__init__(self, key1, unique1, unique2, unique3)
                Parent2Global.__init__(self, key2, unique4, unique5, unique6)

                # Set key3
                self.key3 = key3

                # Set unique fields
                self.unique7 = unique7
                self.unique8 = unique8
                self.unique9 = unique9

            # Define PyOb Meta
            class PyObMeta:

                # Set keys
                keys = ("key3",)

                # Set unique fields
                unique = ("unique7", ("unique8", "unique9"))

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
        """Ensures that the getattr dunder method behaves as expected"""

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

        class A(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

            # Set JPN as a class attribute
            JPN = _JPN

            # Define init method
            def __init__(self, THA, iso3):
                """Init Method"""

                # Set instance attributes
                self.THA = THA
                self.iso3 = iso3

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = ("iso3",)

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
        """Ensure that user-defined attributes are initialized as expected"""

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

            class A1(PyOb):
                """A test class to ensure that PyOb attributes are initialized"""

                # Define PyOb Meta
                class PyObMeta:

                    # Define keys
                    keys = itertype((KEY_1, KEY_2))

                    # Define unique fields
                    unique = itertype((UNIQUE_1, itertype((UNIQUE_2, UNIQUE_3))))

            class A2(PyOb):
                """A test class to ensure that PyOb attributes are initialized"""

                # Define PyOb Meta
                class PyObMeta:

                    # Define keys
                    keys = itertype((KEY_1, KEY_2, KEY_2))

                    # Define unique fields
                    unique = itertype(
                        (UNIQUE_1, UNIQUE_1, itertype((UNIQUE_2, UNIQUE_3, UNIQUE_3)))
                    )

                    # NOTE: Duplicate values should be removed

            # Iterate over A classes
            for A in (A1, A2):

                # Assert that keys are converted to tuple
                self.assertEqual(A.PyObMeta.keys, (KEY_1, KEY_2))

                # Assert that unique fields are converted to tuples
                self.assertEqual(A.PyObMeta.unique, (UNIQUE_1, (UNIQUE_2, UNIQUE_3)))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = {KEY_1, KEY_2}

                # Define unique fields
                unique = (UNIQUE_1, {UNIQUE_2, UNIQUE_3})

        # Assert that keys are converted to tuple
        self.assertTrue(
            type(B.PyObMeta.keys) is tuple
            and len(B.PyObMeta.keys) == 2
            and all([k in B.PyObMeta.keys for k in (KEY_1, KEY_2)])
        )

        # Assert that unique fields are converted to tuples
        self.assertTrue(
            len(B.PyObMeta.unique) == 2
            and B.PyObMeta.unique[0] == UNIQUE_1
            and all([u in B.PyObMeta.unique[1] for u in (UNIQUE_2, UNIQUE_3)])
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ C
        # └─────────────────────────────────────────────────────────────────────────────

        class C(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = KEY_1

                # Define unique fields
                unique = UNIQUE_1

        # Assert that keys are converted to tuple
        self.assertEqual(C.PyObMeta.keys, (KEY_1,))

        # Assert that unique fields are converted to tuples
        self.assertEqual(C.PyObMeta.unique, (UNIQUE_1,))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ D
        # └─────────────────────────────────────────────────────────────────────────────

        class D(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

            # Define PyOb Meta
            class PyObMeta:

                # Set keys to None
                keys = None

                # Set unique to None
                unique = None

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ E
        # └─────────────────────────────────────────────────────────────────────────────

        class E(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

            # Define PyOb Meta
            class PyObMeta:

                # Set keys to None
                keys = ["a", "b"]

                # Set unique to None
                unique = [["c", "d"], "e"]

                # Define a pre-setter method for a field
                def pre_a(self, value):
                    """Pre-setter for the a field"""
                    return value

                # Define a post-setter method for b field
                def post_b(self, value):
                    """Post-setter for the a field"""
                    return value

        # Iterate over test classes
        for Class in (D, E):

            # Iterate over iterable PyOb attributes in class
            for value in (Class.PyObMeta.keys, Class.PyObMeta.unique):

                # Assert that the value is initialized to a tuple
                self.assertIs(type(value), tuple)

            # Ensure that all items in unique are a tuple or string
            self.assertTrue(
                all([type(i) in (str, tuple) for i in Class.PyObMeta.unique])
            )

        # Assert that the pre-setter method in E class is cached
        self.assertTrue("a" in E.PyObMeta.pre)

        # Assert that the post-setter method in E class is cached
        self.assertTrue("b" in E.PyObMeta.post)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ F
        # └─────────────────────────────────────────────────────────────────────────────

        class F(PyOb):
            """A test class to ensure that PyOb attributes are initialized"""

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
            self.assertEqual(F.PyObMeta.type_hints[field], field_type)

        # Assert that the obs property points to the store
        self.assertEqual(id(F.obs), id(F.PyObMeta.store))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST INIT CLASS ATTRIBUITE INHERITANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_init_class_attribute_inheritance(self):
        """Ensure that user-defined attributes are inherited as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CONSTANTS
        # └─────────────────────────────────────────────────────────────────────────────

        KEY_A = "key_a"
        KEY_B = "key_b"
        KEY_C = "key_c"
        KEY_D = "key_d"

        UNIQUE_A1 = "unique_a1"
        UNIQUE_A2 = ("unique_a2a", "unique_a2b")
        UNIQUE_B1 = "unique_b1"
        UNIQUE_B2 = ("unique_b2a", "unique_b2b")
        UNIQUE_C1 = "unique_c1"
        UNIQUE_C2 = ("unique_c2a", "unique_c2b")
        UNIQUE_D1 = "unique_d1"
        UNIQUE_D2 = ("unique_d2a", "unique_d2b")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_A,)

                # Define unique fields
                unique = (UNIQUE_A1, UNIQUE_A2)

        class B(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_B,)

                # Define unique fields
                unique = (UNIQUE_B1, UNIQUE_B2)

        class C(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_C,)

                # Define unique fields
                unique = (UNIQUE_C1, UNIQUE_C2)

        class D(B, C):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_D,)

                # Define unique fields
                unique = (UNIQUE_D1, UNIQUE_D2)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHECK INHERITANCE
        # └─────────────────────────────────────────────────────────────────────────────

        # Iterate over classes
        for Class, keys, unique in (
            (A, (KEY_A,), (UNIQUE_A1, UNIQUE_A2)),
            (B, (KEY_A, KEY_B), (UNIQUE_A1, UNIQUE_A2, UNIQUE_B1, UNIQUE_B2)),
            (
                C,
                (KEY_A, KEY_C),
                (UNIQUE_A1, UNIQUE_A2, UNIQUE_C1, UNIQUE_C2),
            ),
            (
                D,
                (KEY_A, KEY_B, KEY_C, KEY_D),
                (
                    UNIQUE_A1,
                    UNIQUE_A2,
                    UNIQUE_B1,
                    UNIQUE_B2,
                    UNIQUE_C1,
                    UNIQUE_C2,
                    UNIQUE_D1,
                    UNIQUE_D2,
                ),
            ),
        ):

            # Assert that keys are correctly inherited
            self.assertEqual(Class.PyObMeta.keys, keys)

            # Assert that unique fields are correctly inherited
            self.assertEqual(Class.PyObMeta.unique, unique)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST INIT PREPOST HOOK INHERITANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_init_prepost_hook_inheritance(self):
        """Ensures that prepost hooks are inherited as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT
        # └─────────────────────────────────────────────────────────────────────────────

        class Parent(PyOb):
            """Parent Class"""

            # Define init method
            def __init__(self, multiplied):

                # Set multiplied
                self.multiplied = multiplied

            # Define PyOb Meta
            class PyObMeta:

                # Define pre hook method
                def pre_multiplied(instance, value):
                    return value * 2

                # Define post hook method
                def post_multiplied(instance, value):
                    return 2

        # Create new parent instance
        parent = Parent(3)

        # Assert that multiplied field is multiplied
        self.assertEqual(parent.multiplied, 6)

        # Assert that post hook returns 2
        self.assertEqual(parent.PyObMeta.post_multiplied(parent, None), 2)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class Child(Parent):
            """Child Class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define pre hook method
                def pre_multiplied(self, value):
                    return value * 3

                # Define post hook method
                def post_multiplied(self, value):
                    return 3

        # Create new child instance
        child = Child(3)

        # Assert that multiplied field is multiplied
        self.assertEqual(child.multiplied, 9)

        # Assert that post hook returns 2
        self.assertEqual(child.PyObMeta.post_multiplied(child, None), 3)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST INSTANCE CHECK
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_instancecheck(self):
        """Ensures that the instancecheck dunder behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A AND B
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

        class B(A):
            """A PyOb test class"""

        # Create B instance
        b = B()

        # Assert that B() is an instance of A
        self.assertAllEqual(isinstance(b, A), A.__instancecheck__(b), True)

        # Localize A and B
        _A, _B = localize(A, B)

        # Create _B instance
        _b = _B()

        # Assert that _B() is an instance of _A
        self.assertAllEqual(isinstance(_b, _A), _A.__instancecheck__(_b), True)

        # Assert that _B() is an instance of A
        self.assertAllEqual(isinstance(_b, A), A.__instancecheck__(_b), True)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST POW
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_pow(self):
        """Ensures that the pow dunder method behaves as expected"""

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
        """Ensures that the rshift dunder method behaves as expected"""

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
