import math

def encrypt(text: str, key: int) -> str:
    rows = [text[i:i+key] for i in range(0, len(text), key)]
    out = []
    for col in range(key):
        for r in rows:
            if col < len(r):
                out.append(r[col])
    return ''.join(out)

def decrypt(cipher: str, key: int) -> str:
    cols = key
    rows = math.ceil(len(cipher) / cols)
    shaded = cols * rows - len(cipher)  
    col_lens = [rows] * cols
    for i in range(shaded):
        col_lens[cols - 1 - i] -= 1

    parts = []
    idx = 0
    for L in col_lens:
        parts.append(cipher[idx:idx+L]); idx += L

    out = []
    for r in range(rows):
        for c in range(cols):
            if r < len(parts[c]):
                out.append(parts[c][r])
    return ''.join(out)
