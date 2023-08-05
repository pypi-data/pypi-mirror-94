"The operations of number_comparator."

__all__ = ["reverseNumber",
           "reverseFloat",
           "average"]


"At first, try to import Colorama for Warnings."
from number_comparator.data.colors import Fore


def reverseNumber(n):
    "Get the reverse number for integers."
    if isinstance(n, type(1.0)):
        print(Fore.YELLOW + "WARNING: The 'reverseNumber' is only for integers. "
                       "The float number will be\n" + "truncated to integer. "
                       "If you are not agree, use function 'reverseFloat'.")
        n = int(n)
    try:
        if n < 0:
            return n + (n + n)
        elif n > 0:
            return n - (n + n)
        elif n == 0:
            raise ValueError(f"Cannot operate zero values")
        else:
            return None
    except (TypeError, ValueError):
        raise TypeError(f"'reverseNumber' function is only available for int or float numbers, not %s" % n)


def reverseFloat(n):
    "Get the reverse number for float numbers."
    if not isinstance(n, type(1.0)):
        raise TypeError(f"'Expected float numbers, not %s" % n)
    if n > 0.0:
        # Positive to negative
        return float("-" + str(n))
    elif n < 0.0:
        # Negative to positive
        return float(str(n)[1:])
    elif n == 0.0:
        raise ValueError(f"Cannot operate zero values")


def average(*nums):
    "Get the average from a tuple."
    l = []
    for num in nums:
        if not isinstance(num, (type(1), type(1.0))):
            raise TypeError(f"Expected int/float numbers, got %s" % num)
        l.append(num)
    t = None
    for n in l:
        if t is None:
            t = n
        else:
            t = t + n
    return t / len(l)
