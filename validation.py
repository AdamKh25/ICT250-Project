SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."

def require_text(x: str) -> str:
    if not isinstance(x, str) or x == "":
        raise ValueError("Text must be a non-empty string.")
    return x

def require_int(x) -> int:
    try:
        return int(x)
    except Exception:
        raise ValueError("Expected an integer.")

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def mod_inverse(a: int, m: int) -> int | None:
    a %= m
    if gcd(a, m) != 1:
        return None
    t, nt = 0, 1
    r, nr = m, a
    while nr:
        q = r // nr
        t, nt = nt, t - q * nt
        r, nr = nr, r - q * nr
    return t % m

def is_valid_affine_a(a: int) -> bool:
    return gcd(a, 26) == 1

def make_affine_key(a: int, b: int) -> int:
    return a * 26 + (b % 26)
