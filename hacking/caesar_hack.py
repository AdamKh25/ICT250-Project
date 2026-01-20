from validation import SYMBOLS
from analysis.english_score import score_english
from ciphers.caesar import decrypt

def hack(ciphertext: str, top_k: int = 5):
    cands = []
    for key in range(26):
        pt = decrypt(ciphertext, key) 
        cands.append((score_english(pt), key, pt))
    cands.sort(reverse=True, key=lambda x: x[0])
    best = cands[0]
    return best[2], best[1], cands[:top_k]
