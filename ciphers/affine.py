from validation import SYMBOLS

def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def _modinv(a: int, m: int) -> int | None:
    a %= m
    if _gcd(a, m) != 1:
        return None
    t, nt = 0, 1
    r, nr = m, a
    while nr:
        q = r // nr
        t, nt = nt, t - q * nt
        r, nr = nr, r - q * nr
    return t % m

def get_key_parts(key: int) -> tuple[int, int]:
    a = key // 26
    b = key % 26
    return a, b

def encrypt(text: str, key: int) -> str:
    a, b = get_key_parts(key)
    if _gcd(a, 26) != 1:
        raise ValueError("Invalid key: gcd(a,26) must be 1")
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            p = ord(ch) - 65
            out.append(chr((a * p + b) % 26 + 65))
        elif 'a' <= ch <= 'z':
            p = ord(ch) - 97
            out.append(chr((a * p + b) % 26 + 97))
        else:
            out.append(ch if ch in SYMBOLS else ch)
    return ''.join(out)

def decrypt(text: str, key: int) -> str:
    a, b = get_key_parts(key)
    if _gcd(a, 26) != 1:
        raise ValueError("Invalid key: gcd(a,26) must be 1")
    inv = _modinv(a, 26)
    if inv is None:
        raise ValueError("Invalid key: no modular inverse for a")
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            c = ord(ch) - 65
            out.append(chr((inv * (c - b)) % 26 + 65))
        elif 'a' <= ch <= 'z':
            c = ord(ch) - 97
            out.append(chr((inv * (c - b)) % 26 + 97))
        else:
            out.append(ch if ch in SYMBOLS else ch)
    return ''.join(out)
