# hacking/caesar_hack.py
from ciphers import caesar

# Very simple English-like scoring
COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")

def score(text: str) -> int:
    t = text.upper()
    s = t.count(" ")
    for w in COMMON_WORDS:
        s += t.count(w)
    return s

def hack(ciphertext: str):
    """
    Try all 26 Caesar keys and return:
      best_plaintext, best_key, candidates_list

    candidates_list is a list of dicts like:
      {"key": k, "plaintext": text, "score": s}
    """
    best_plain = ""
    best_key = 0
    best_score = -1
    candidates = []

    for key in range(26):
        pt = caesar.decrypt(ciphertext, key)
        s = score(pt)
        candidates.append({"key": key, "plaintext": pt, "score": s})
        if s > best_score:
            best_score = s
            best_plain = pt
            best_key = key

    return best_plain, best_key, candidates
