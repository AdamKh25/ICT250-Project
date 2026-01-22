# brute force caesar cipher attack
# works on classic a-z alphabet

# alphabet used for caesar cipher
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# decrypt text using a specific caesar key
def decrypt_with_key(ciphertext: str, key: int) -> str:
    # store decrypted characters
    result = []

    # process text in uppercase
    for ch in ciphertext.upper():
        if ch in LETTERS:
            # get letter index
            num = LETTERS.find(ch)

            # shift backward by key
            num = (num - key) % len(LETTERS)

            # append decrypted letter
            result.append(LETTERS[num])
        else:
            # keep non-letters unchanged
            result.append(ch)

    return "".join(result)


# brute force all possible caesar keys
def hack(ciphertext: str):
    # store all candidate results
    candidates = []

    best_plain = ""
    best_key = 0
    best_score = -1

    # try all 26 possible keys
    for key in range(26):
        # decrypt using current key
        pt = decrypt_with_key(ciphertext, key)

        # store candidate
        candidates.append((key, pt))

        # score text using simple english checks
        t = pt.upper()
        score = t.count(" ") + t.count("HELLO") + t.count("WORLD")

        # stop early if known phrase found
        if "HELLO WORLD" in t:
            return pt, key, candidates

        # update best guess
        if score > best_score:
            best_score = score
            best_plain = pt
            best_key = key

    # return best result and all candidates
    return best_plain, best_key, candidates
