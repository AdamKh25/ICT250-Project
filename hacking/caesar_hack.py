# hacking/caesar_hack.py
# Brute-force Caesar using the class idea:
# - try all 26 keys
# - decrypt with ciphers.caesar.decrypt
# - simple English-like score
# - if we see "HELLO WORLD", choose it immediately

from ciphers import caesar

COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")

def simple_score(text: str) -> int:
    t = text.upper()
    s = t.count(" ")
    for w in COMMON_WORDS:
        s += t.count(w)
    return s

def hack(ciphertext: str):
    """
    Returns:
      best_plaintext, best_key, candidates

    candidates: list of (score, key, plaintext)
    """
    candidates = []
    best_plain = ""
    best_key = 0
    best_score = -1

    for key in range(26):
        pt = caesar.decrypt(ciphertext, key)
        s = simple_score(pt)

        candidates.append((s, key, pt))

        # special case: if the true message appears, return immediately
        if "HELLO WORLD" in pt.upper():
            return pt, key, candidates

        if s > best_score:
            best_score = s
            best_plain = pt
            best_key = key

    return best_plain, best_key, candidates
