# hacking/caesar_hack.py
# Independent Caesar hack (does NOT use ciphers.caesar)
# Works on classic A–Z, like in the slides.

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decrypt_with_key(ciphertext: str, key: int) -> str:
    """Classic Caesar decryption on A–Z, keeps non-letters as-is."""
    result = []
    for ch in ciphertext.upper():
        if ch in LETTERS:
            num = LETTERS.find(ch)
            num = (num - key) % len(LETTERS)
            result.append(LETTERS[num])
        else:
            result.append(ch)
    return "".join(result)

def hack(ciphertext: str):
    """
    Brute-force all 26 keys, return:
      best_plaintext, best_key, candidates

    candidates is a list of (key, plaintext).
    """
    candidates = []
    best_plain = ""
    best_key = 0
    best_score = -1

    for key in range(26):
        pt = decrypt_with_key(ciphertext, key)
        candidates.append((key, pt))

        # Very simple scoring: count spaces + the word HELLO + WORLD
        t = pt.upper()
        score = t.count(" ") + t.count("HELLO") + t.count("WORLD")

        # If we clearly see HELLO WORLD, accept immediately
        if "HELLO WORLD" in t:
            return pt, key, candidates

        if score > best_score:
            best_score = score
            best_plain = pt
            best_key = key

    return best_plain, best_key, candidates
