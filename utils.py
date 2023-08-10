from fractions import Fraction

def prime_field(p) -> list:
    """Returns a finite field with p elements."""
    return list(range(p))

# def prime_field_value(x, p) -> int:
    

def get_prime(n) -> int:
    """Returns a prime greater than n and k"""
    p = n + 1
    while not is_prime(p):
        p += 1
    return p

def is_prime(n) -> bool:
    """Returns True if n is prime, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True

def prime_field_group(g, p) -> list:
    """Returns a finite field group with p elements."""
    return list(set([g ** i % p for i in range(p)]))


def mod_inverse(A, M) -> int:
        for X in range(1, M):
            if (((A % M) * (X % M)) % M == 1):
                return X
        return -1


def mod_inverse2(a, m):
    m0 = m
    t, q = 0, 0
    x0, x1 = 0, 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = x0
        x0 = x1 - q * x0
        x1 = t

    if x1 < 0:
        x1 += m0

    return x1
def float_to_ratio(flt):
    if int(flt) == flt:        # to prevent 3.0 -> 30/10
        return int(flt), 1
    flt_str = str(flt)
    flt_split = flt_str.split('.')
    numerator = int(''.join(flt_split))
    denominator = 10 ** len(flt_split[1])
    return numerator, denominator

def field_prime_value(num, p):
    num = Fraction(num)
    numerator = num.numerator
    denominator = num.denominator if num >= 0 else -num.denominator
    inv_denominator = mod_inverse(denominator, p)
    field_prime_val = (numerator * inv_denominator) % p
    return field_prime_val

# a = input("Enter num: ")
# p = int(input("Enter p: "))
# print(field_prime_value(Fraction(a), p))
