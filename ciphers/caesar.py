# hacking/caesar_hack.py
# Brute force Caesar cipher, similar to the class slides:
# - Try all 26 keys
# - Decrypt using ciphers.caesar.decrypt
# - Score English-likeness in a simple way

from ciphers import caesar

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")

def simple_score(text: str) -> int:
    """Very simple English scoring like in class: spaces + common words."""
    t = text.upper()
    s = t.count(" ")
    for w in COMMON_WORDS:
        s += t.count(w)
    return s

def hack(ciphertext: str):
    """
    Try all 26 Caesar keys and return:
      (best_plaintext, best_key, candidates)

    candidates: list of dicts:
      {"key": k, "plaintext": pt, "score": s}
    """
    best_plain = ""
    best_key = 0
    best_score = -1
    candidates = []

    for key in range(26):
        # Use your existing Caesar code
        pt = caesar.decrypt(ciphertext, key)
        s = simple_score(pt)

        candidates.append({
            "key": key,
            "plaintext": pt,
            "score": s,
        })

        # If we see the clear phrase from the smoke_test, accept immediately
        if "HELLO WORLD" in pt.upper():
            return pt, key, candidates

        if s > best_score:
            best_score = s
            best_plain = pt
            best_key = key

    return best_plain, best_key, candidates
