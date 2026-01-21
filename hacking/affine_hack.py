# hacking/affine_hack.py
from ciphers import affine
import math

COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")

def score(text: str) -> int:
    t = text.upper()
    s = t.count(" ")
    for w in COMMON_WORDS:
        s += t.count(w)
    return s

def hack(ciphertext: str):
    """
    Try all valid (a, b) for Affine over 26 letters.
    Return:
      best_plaintext, (best_a, best_b), candidates_list

    candidates_list is a list of dicts like:
      {"a": a, "b": b, "plaintext": text, "score": s}
    """
    M = 26
    # valid a values: 1..25, odd, gcd(a,26)==1
    validA = [a for a in range(1, M, 2) if math.gcd(a, M) == 1]

    best_plain = ""
    best_a = None
    best_b = None
    best_score = -1
    candidates = []

    for a in validA:
        for b in range(M):
            key = a * M + b  # same packing as in affine cipher code
            try:
                pt = affine.decrypt(ciphertext, key)
            except Exception:
                continue
            s = score(pt)
            candidates.append({"a": a, "b": b, "plaintext": pt, "score": s})
            if s > best_score:
                best_score = s
                best_plain = pt
                best_a, best_b = a, b

    return best_plain, (best_a, best_b), candidates
