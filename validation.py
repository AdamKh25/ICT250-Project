# validation.py
# Minimal helpers kept so older code/tests can still `import validation`.

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = 26  # modulus for A–Z ciphers

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def mod_inverse(a: int, m: int) -> int | None:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_valid_affine_a(a: int) -> bool:
    return gcd(a, M) == 1

def make_affine_key(a: int, b: int) -> int:
    # pack (a,b) into one integer key (used by some code paths)
    return a * M + (b % M)

def get_affine_parts(key: int) -> tuple[int, int]:
    return key // M, key % M
