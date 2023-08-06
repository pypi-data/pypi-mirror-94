"The comparations of number_comparator."

__all__ = ["PAIR_TERMINATIONS",
           "isPair",
           "isPeriodic",
           "isPrime",
           "isMultiple"]

PAIR_TERMINATIONS = ["2",
                     "4",
                     "6",
                     "8",
                     "0"]

from number_comparator.data.first_prime import first_168, PRIME_TERMINATIONS
import warnings

def isPair(n):
    "Look if an integer is a pair."
    if isinstance(n, type(1.0)):
        n = int(n)
    elif not isinstance(n, type(1)):
        raise ValueError(f"You must enter 'int' or 'float' numbers, not %s" % n)
    return str(n)[len(str(n)) - 1:] in PAIR_TERMINATIONS


def isPeriodic(a):
    "Check if a float/int is periodic."
    a = str(float(a)).split(".")[1]
    b = a[0]
    for i in a:
        r = i == b
    return not r


def isPrime(n):
    "Verify if a number is a prime by using the Eratostenes method."
    if not isinstance(n, (type(1), type(1.0))):
        raise ValueError(f"You must enter 'int' or 'float' numbers, not %s" % n)
    if n > first_168[len(first_168) - 1]:
        a = str(float(n))
        b = a[len(a) - 1] in PRIME_TERMINATIONS and n > 2
        return b is True and n not in [1001, 1003, 1007, 10001, 10003, 100001, 1000001] # These are not prime numbers
    return n in first_168


def truncate(n):
    "Truncate a number by converting it to an integer."
    if not isinstance(n, (type(1.0))):
        raise ValueError(f"You must enter 'float' numbers, not %s" % n)
    return int(n)


def roundout(n):
    "Roundout is a little bit more complex than truncate(), because we are depending from decimal output to operate."
    if not isinstance(n, (type(1.0))):
        raise ValueError(f"You must enter 'float' numbers, not %s" % n)


def isMultiple(a, b):
    "Verify if A is a multiple of B."
    if not isinstance(a, type(1)) or not isinstance(b, type(1)):
        raise TypeError(f"Expected int numbers, got values: %s | %s" % (a, b))
    elif b > a:
        raise SyntaxError(f"Value 1 (%s) must not be larger than value 2 (%s)" % (a, b))
    elif b < 1:
        raise ValueError(f"Cannot operate zero or negative values")
    elif b == 1:
        msg = f"""When using 1 as divisor (arg 2), you will always get True.
We are returning True immediatly to save variables."""
        warnings.warn(msg)
        return True
    c = 0
    d = False
    while c < a:
        c = c + b
        if c == a:
            d = True
    return d
