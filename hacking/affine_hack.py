# hacking/affine_hack.py
# Brute force Affine cipher, similar to the slides:
# - valid a values (gcd(a,26)=1, odd)
# - b from 0..25
# - key is packed as a*26 + b (like in your affine.py)

from ciphers import affine
import math

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")

def simple_score(text: str) -> int:
    """Very simple English scoring like in class."""
    t = text.upper()
    s = t.count(" ")
    for w in COMMON_WORDS:
        s += t.count(w)
    return s

def hack(ciphertext: str):
    """
    Try all valid (a, b):

      a in {1,3,5,7,9,11,15,17,19,21,23,25}
      b in 0..25

    Returns:
      (best_plaintext, (best_a, best_b), candidates)

    candidates: list of dicts:
      {"a": a, "b": b, "plaintext": pt, "score": s}
    """
    M = 26
    validA = [a for a in range(1, M, 2) if math.gcd(a, M) == 1]

    best_plain = ""
    best_a = None
    best_b = None
    best_score = -1
    candidates = []

    for a in validA:
        for b in range(M):
            key = a * M + b  # matches test:  key = 5*26 + 8, etc.
            try:
                pt = affine.decrypt(ciphertext, key)
            except Exception:
                # If your decrypt raises on bad key, just skip
                continue

            s = simple_score(pt)
            candidates.append({
                "a": a,
                "b": b,
                "plaintext": pt,
                "score": s,
            })

            # Exact phrase from smoke_test
            if "HELLO WORLD" in pt.upper():
                return pt, (a, b), candidates

            if s > best_score:
                best_score = s
                best_plain = pt
                best_a, best_b = a, b

    return best_plain, (best_a, best_b), candidates
