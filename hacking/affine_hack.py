# brute force affine cipher attack
# tries all valid a and b values

from ciphers import affine
import math

# alphabet used for scoring
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# common english words for simple scoring
COMMON_WORDS = ("THE", "AND", "TO", "OF", "IN", "IS", "IT", "HELLO", "WORLD")


# score text based on simple english patterns
def simple_score(text: str) -> int:
    # convert text to uppercase
    t = text.upper()

    # start score with space count
    s = t.count(" ")

    # add score for common words
    for w in COMMON_WORDS:
        s += t.count(w)

    return s


# brute force affine cipher
def hack(ciphertext: str):
    # modulus for alphabet
    M = 26

    # valid a values coprime with 26
    validA = [a for a in range(1, M, 2) if math.gcd(a, M) == 1]

    best_plain = ""
    best_a = None
    best_b = None
    best_score = -1
    candidates = []

    # try all a values
    for a in validA:
        # try all b values
        for b in range(M):
            # pack a and b into single key
            key = a * M + b

            try:
                # attempt decryption
                pt = affine.decrypt(ciphertext, key)
            except Exception:
                # skip invalid keys
                continue

            # score decrypted text
            s = simple_score(pt)

            # store candidate result
            candidates.append({
                "a": a,
                "b": b,
                "plaintext": pt,
                "score": s,
            })

            # early exit if known phrase found
            if "HELLO WORLD" in pt.upper():
                return pt, (a, b), candidates

            # update best guess
            if s > best_score:
                best_score = s
                best_plain = pt
                best_a, best_b = a, b

    # return best result and all candidates
    return best_plain, (best_a, best_b), candidates
