<h1 align="center">_PyOb</h1>

<p align="center">
    <img width="241" height="221" src="./media/pyob-hierarchy.png" alt="Yank Logo">
</p>

PyOb is a high-level runtime object manager for Python 3 and above.

This project is under heavy development and not yet stable. It should not be used in a production environment.

More feature documentation as unit tests are completed...


## Installation

The Python Package Index (PyPI) can be used to install PyOb.

```
pip install pyob
```

## Basic Usage

Convert your Python classes into PyOb classes by simply inheriting from `pyob.Ob`:

```python
from pyob import Ob

class Country(Ob):
    """ A PyOb class to represent country objects """

    _str = "name"             # Optional PyOb attribute for a pretty str representation
    _keys = ("iso2", "iso3")  # Optional PyOb attribute defining unique key accessors

    def __init__(self, name: str, iso2: str, iso3: str):  # Optional type hints on attributes
        """ Init Method """

        self.name = name
        self.iso2 = iso2
        self.iso3 = iso3
```

Create object instances as you would any other Python class:

```python
tha = Country(name="Thailand",      iso2="TH", iso3="THA")
usa = Country(name="United States", iso2="US", iso3="USA")
```

Notice that object instances are automatically tracked by an object store during runtime:

```python
Country.obs

# <CountryStore: 2 [<Country: Thailand>, <Country: United States>]>

Country.obs.count()

# 2
```

Sort object instances by one or multiple fields:

```python
Country.obs.sort("name")

# <CountrySet: 2 [<Country: Thailand>, <Country: United States>]>

Country.obs.sort("-name")

# <CountrySet: 2 [<Country: United States>, <Country: Thailand>]>

Country.obs.sort("name", "iso3")

# <CountrySet: 2 [<Country: Thailand>, <Country: United States>]>
```

Filter object instances by one or multiple fields:

```python
Country.obs.filter(name="Thailand", iso3="THA")

# <CountrySet: 1 [<Country: Thailand>]>
```

Retrieve objects by unique key accessors:

```python
Country.obs >> "TH"   # ISO2

# <Country: Thailand>

Country.obs >> "USA"  # ISO3

# <Country: United States>
```

Key accessors can also be applied as attributes given that they conform to valid dot syntax:

```python
Country.obs.USA

# <Country: United States>
```

Type hints on instance attributes will be enforced at runtime by default:

```python
chn = Country(name="China", iso2=35, iso3="CHN")

# pyob.exceptions.InvalidTypeError: Country.iso2 expects a value of type <class 'str'> but got: 35 (<class 'int'>)

usa.iso2 = True

# pyob.exceptions.InvalidTypeError: Country.iso2 expects a value of type <class 'str'> but got: True (<class 'bool'>)
```

See PyOb's [feature guide](#feature-guide) for further explanation of these features plus many more.

## Feature Guide

<details>
<summary><strong>Objects</strong></summary>

<br/>

For demonstration purposes, we'll go ahead and create a PyOb class to represent country objects:

```python
# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import Ob

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COUNTRY
# └─────────────────────────────────────────────────────────────────────────────────────

class Country(Ob):
    """ A PyOb class to represent country objects """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Set string field
    _str = "name"

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        name: str,
        iso2: str,
        iso3: str,
    ):
        """ Init Method """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Set country name
        self.name = name

        # Set ISO codes, e.g. US, USA
        self.iso2 = iso2
        self.iso3 = iso3
```

In this case, we assume that all `Country` objects should have a name, as well as an ISO2 and ISO3 alpha code.

We've also made use of our first PyOb attribute, `_str`, which informs PyOb that `Country.name` should be used when generating a `Country` instance's string representation so that it looks like this:

```
<Country: United States>
```

... instead of like this:

```
<Country: 0x7f1d2e5e4ac0>
```

Note that the type hints in the `Country` init method are optional but recommended if your wish to take advantage of PyOb's convenient [runtime type checking feature](#runtime-type-checking).

</details>

<details>
<summary><strong>Object Sets</strong></summary>

<br/>

An object set (`pyob.ObSet`) represents a collection of object instances.

Let's create two `Country` instances representing North and South Korea:

```python
prk = Country(name="North Korea", iso2="KP", iso3="PRK")
kor = Country(name="South Korea", iso2="KR", iso3="KOR")
```

We can combine these instances into an object set to represent the two Koreas:

```python
prk + kor

# <CountrySet: 2 [<Country: North Korea>, <Country: South Korea>]>
```

We could create the same object set in the following ways:

```python
Country.Set() + prk + kor
Country.Set() + [prk, kor]

# <CountrySet: 2 [<Country: North Korea>, <Country: South Korea>]>
```

As can be inferred in the above example, `Country.Set()` creates an empty `Country` object set to which `Country` instances or other `Country` object sets can be added.

The behavior of object sets is list-like in that they can contain more than one reference to the same object:

```python
prk + kor + kor

# <CountrySet: 3 [<Country: North Korea>, <Country: South Korea>, <Country: South Korea>]>
```

</details>


<details>
<summary><strong>Object Stores</strong></summary>

<br/>

All PyOb classes are initialized with an object store (`pyob.ObStore`) that keeps track of object instances initialized during runtime. For those familiar with databases, objects are to rows as object stores are to tables.

We can verify that the `Country` object store contains no `Country` instances upon class definition:

```python
class Country(Ob):
    """ A PyOb class to represent country objects """
    # [ ... ]

Country.obs

# <CountryStore: 0 []>
```

Let's now create two country instances:

```python
tha = Country(name="Thailand",      iso2="TH", iso3="THA")
usa = Country(name="United States", iso2="US", iso3="USA")
```

Without doing anything further, we'll notice that our `CountryStore` now contains two `Country` instances:

```python
Country.obs

# <CountryStore: 2 [<Country: Thailand>, <Country: United States>]>
```

**Note:** Object stores are initialized at and persist throughout each runtime meaning that any file or script using the `Country` class will share a single object store regardless of where in your project the class is used.

Under most circumstances, this is not an issue (and may even be desired). However, to ensure that a given file or script uses an isolated object store, consider cloning the PyOb class first, which will initialize a clean object store.

```python
Country.obs

# <CountryStore: 2 [<Country: Thailand>, <Country: United States>]>

class CountryIsolated(Country):
    """ A clone of the Country PyOb class with a clean object store """

CountryIsolated.obs

# <CountryIsolatedStore: 0 []>
```

</details>

<details>
<summary><strong>Object Class Labels</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>List-like Index Slicing</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>Dict-like Key Accessors</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>Set-like Operation Logic</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>ORM-like Sort Methods</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>ORM-like Filter Methods</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary><strong>ORM-like Descriptive Methods</strong></summary>

<br/>

Documentation Pending Tests...

</details>

<details>
<summary id="runtime-type-checking"><strong>Runtime Type Checking</strong></summary>

<br/>

Because our definition of `Country` includes type hints on its init method arguments, PyOb will automatically check their type before setting them as instance attributes, and raise an error if it encounters an incorrect type:

```python
chn = Country(name="China", iso2=35, iso3="CHN")

# pyob.exceptions.InvalidTypeError: Country.iso2 expects a value of type <class 'str'> but got: 35 (<class 'int'>)
```

Conveniently, runtime type checking is also performed when setting instance attributes on existing objects:

```python
usa.iso2 = True

# pyob.exceptions.InvalidTypeError: Country.iso2 expects a value of type <class 'str'> but got: True (<class 'bool'>)
```

In cases where the init method expects a type that will change before being set as an instance attribute, a class-level type hint will take precedence in the type check:

```python
# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ MY OBJECT
# └─────────────────────────────────────────────────────────────────────────────────────

class MyObject(Ob):

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TYPE HINTS
    # └─────────────────────────────────────────────────────────────────────────────────

    number: int

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, number: str):
        """ Init Method """

        # Convert number to int
        number = int(number)

        # Set number
        self.number = number

# Create an object instance
my_object = MyObject(number="50")  # OK

# NOTE: The init method type hint can simply be omitted here if it isn't used for anything else
```

Note that PyOb utilizes the Python [typeguard](https://github.com/agronholm/typeguard) lubrary to perform these checks. Refer to the typeguard documentation for more information on type support and methodology.

Runtime type checking can be disabled with the following PyOb attribute:

```python
# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ MY OBJECT
# └─────────────────────────────────────────────────────────────────────────────────────

class MyObject(Ob):

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Disable type checking
    _disable_type_checking = True
```

</details>

## Attribute Reference

| Attribute              | Description                                                                           | Default | e.g.             |
|------------------------|---------------------------------------------------------------------------------------|---------|------------------|
| _str                   | The field used to generate a string representation of an object instance              | None    | "name"           |
| _label_singular        | The label used to represent an object class in singular form                          | None    | "Country"        |
| _label_plural          | The label used to represent an object class in plural form                            | None    | "Countries"      |
| _keys                  | The fields used as unique key accessors for instances in an object set or object store             | None    | ("iso2", "iso3") |
| _disable_type_checking | Whether to disable runtime type checking on instance attributes                       | False   | True             |

### More feature documentation as unit tests are completed...
