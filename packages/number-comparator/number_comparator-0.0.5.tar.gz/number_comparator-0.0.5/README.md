# number_comparator

A numeric comparator package, built by Diego Ramirez.

## Introduction

The number_comparator package can compare if a number is a:

- Prime
- Pair
- Periodic
- Multiple of a specific number  *__(new since version 0.0.4)__*

Also, you can operate:

- Average from:
  - Tuples
  - Lists  *__(new since version 0.0.5)__*
- Reverse numbers from:
  - Integers
  - Float

To obtain the package with pip, use one of this commands:

```
pip install number_comparator
pip install number_comparator_[version]_[plat].whl
pip install number_comparator_[version].tar.gz
pip install number_comparator==[version]
pip install --upgrade number_comparator
```

## Release notes

#### What's new in number_comparator 0.0.5

- More accurate functions
  - Some operations corrected or added at function `isMultiple()`

#### What's new in number_comparator 0.0.4

- New features
  - Variable `__license__`
  - New function: `isMultiple()`

#### What's new in number_comparator 0.0.3

- Minor bugs resolved
  - `__version__` variable fixed
  - Some variables fixed at `number_comparator.data.first_prime`
  - Some operations fixed at `number_comparator.operations`:
    - Cleaner functions
- New MANIFEST.in includes:
  - The `setup.py`
  - The license file `LICENSE`
  - The markdown file `README.md`

## Using number_comparator functions

To call the number_comparator library, just type:

```python
from number_comparator import *
```

#### isPair()

The function `isPair(n)` takes a number and returns **True** if the number is a
pair or **False** if not. So, if you type:

```python
print(isPair(20))         # Short number
print(isPair(15))         # Short number
print(isPair(1986031))    # Large number?
```

You'll get this output:

```python
True
False
False
```

#### isPrime()

The prime numbers are numbers that can only be divided by 1 and themselves. To find
if a number is prime, we used many functions:

1. Check if a number is on a list of 168 prime numbers.
2. If the number is larger, check if the termination is 1, 3, 7 or 9

Example: 3, 4, 7.

```python
print(isPrime(3))
print(isPrime(4))
print(isPrime(7))
```

You must get:

```python
True
False
True
```

__NOTE:__ The function `isPrime()` does not support negative numbers. You can convert them
by using the `reverseNumber()` function to operate it later.

#### reverseNumber()

The `reverseNumber()` function converts a negative number to a positive number, and a
positive to a negative. The allowed data type is `int()`.

```python
print(reverseNumber(123))
print(reverseNumber(-123))
```

So, conversions must be:

| Before         | After          |
| :------------- | :------------- |
| 123            | -123           |
| -123           | 123            |

To convert float numbers, use `reverseFloat()`.

#### reverseFloat()

This function has the same function than `reverseNumber()`, but taking a float number:

```python
print(reverseNumber(1.23))
print(reverseNumber(-1.23))
```

#### isPeriodic()

In Python, periodic numbers are infinite float numbers. We are using
this property to see if a number (int or float) is periodic.

For example, `10 / 3` returns a periodic `float()`:

```python
print(isPeriodic(10 / 3))
```

So you'll get the output:

```python
True
```

#### average()

Take an average from a tuple or a group of numbers:

```python
print(average(10, 7, 8, 9)) # As a multiple argument group
```

Getting the output:

```python
8.5
```

#### isMultiple()

Check if a number is a multiple of another number with syntax:

```python
isMultiple(a, b)
```

Here, value `a` is the one to be checked, and `b` is the expected divisor. Taking
this explanation, check the example:

```python
print(isMultiple(15, 5))
print(isMultiple(35, 4))
```

And you must receive output:

```python
True
False
```

__NOTE:__ Function `isMultiple()` __only accepts integers__. If you enter `complex`
or `float` numbers, function will raise a `TypeError`. Check this example:

```python
print(isMultiple(complex(12, 98), 23.87)) # A complex as 'a' and a float as 'b'
```

```
Traceback (most recent call last):
 File .../.../.py, line ..., at <module>
     print(isMultiple(complex(12, 98), 23.87))
 File .../site-packages/number_comparator/comparisons.py, line 62, at isMultiple
         raise TypeError(
                        ^
TypeError: Expected int numbers, got values: 12, 98j | 23.87
```

__NOTE:__ At parameter `b`, `isMultiple()` only accepts numbers positive numbers
larger than 0. Also, when using 1 as `b`, you'll receive:

```
warnings.warn(msg)

0298274hde5t43.UserWarning: When using 1 as divisor (arg 2), you will always get True.
We are returning True immediately to save variables.
```

#### averageFromList()

This function takes a list, extract the numbers, and return the average from them.

Example:

```python
a = [10, complex(12, 8), "dummy string", 9.53, 8, {"a": None}]
print(averageFromList(a))
```

```python
9.17666666666666666
```

At this example, the function ignored the string `"dummy string"`, dictionary `{"a": None}`
and the complex `complex(12, 8)`. __It only takes integers or float numbers.__
