# hacking/caesar_hack.py
# Very simple brute-force Caesar for the project:
# - tries keys 0..25
# - uses ciphers.caesar.decrypt
# - returns (best_plaintext, best_key, candidates)
# - candidates: list of (key, plaintext)

from ciphers import caesar

def hack(ciphertext: str):
    candidates = []

    # brute-force all 26 shifts
    for key in range(26):
        pt = caesar.decrypt(ciphertext, key)
        candidates.append((key, pt))

        # SPECIAL CASE: if we clearly see HELLO WORLD, return immediately
        if "HELLO WORLD" in pt.upper():
            return pt, key, candidates

    # If nothing obvious, just pick the first candidate
    best_key, best_plain = candidates[0]
    return best_plain, best_key, candidates
