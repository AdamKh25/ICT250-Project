from validation import SYMBOLS
from analysis.english_score import score_english
from ciphers.affine import decrypt, _gcd

def _valid_a():
    return [a for a in range(1, 26) if _gcd(a, 26) == 1]

def hack(ciphertext: str, top_k: int = 5):
    cands = []
    for a in _valid_a():
        for b in range(26):
            key = a * 26 + b
            try:
                pt = decrypt(ciphertext, key)
            except Exception:
                continue
            cands.append((score_english(pt), (a, b), pt))
    cands.sort(reverse=True, key=lambda x: x[0])
    best = cands[0]
    return best[2], best[1], cands[:top_k]
