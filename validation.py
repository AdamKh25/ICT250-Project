SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def require_text(name: str, s: str) -> str:
    if not isinstance(s, str) or s.strip() == '':
        raise ValueError(f"{name} must be non-empty string")
    return s.strip()

def require_int(name: str, v: int, min_v: int = 0):
    if not isinstance(v, int):
        raise ValueError(f"{name} must be integer")
    if v < min_v:
        raise ValueError(f"{name} >= {min_v}")
    return v

def mod_inverse(a: int, m: int) -> int:
    from math import gcd
    if gcd(a, m) != 1:
        raise ValueError("No inverse")
    return pow(a, -1, m)
