SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def require_text(name: str, s: str) -> str:
    if not isinstance(s, str) or not s.strip():
        raise ValueError(f"{name} must be non-empty string")
    return s.strip()

def require_int(name: str, v: int, min_v: int = 0) -> int:
    if not isinstance(v, int):
        raise ValueError(f"{name} must be int >= {min_v}")
    if v < min_v:
        raise ValueError(f"{name} must be >= {min_v}")
    return v

def mod_inverse(a: int, m: int = 26) -> int:
    from math import gcd
    if gcd(a, m) != 1:
        raise ValueError("a must be coprime with 26")
    return pow(a
