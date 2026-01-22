# minimal validation helpers for compatibility

# alphabet for a-z ciphers
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# modulus for alphabet size
M = 26


# compute greatest common divisor
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


# find modular inverse of a mod m
def mod_inverse(a: int, m: int) -> int | None:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# check if a is valid for affine cipher
def is_valid_affine_a(a: int) -> bool:
    return gcd(a, M) == 1


# combine a and b into a single affine key
def make_affine_key(a: int, b: int) -> int:
    return a * M + (b % M)


# extract a and b from affine key
def get_affine_parts(key: int) -> tuple[int, int]:
    return key // M, key % M
