from validation import SYMBOLS

def encrypt(text: str, key: str) -> str:
    key = key.upper()
    j = 0
    out = []
    for ch in text:
        if ch.isalpha():
            k = ord(key[j % len(key)]) - 65
            j += 1
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch if ch in SYMBOLS else ch)
    return ''.join(out)

def decrypt(text: str, key: str) -> str:
    key = key.upper()
    j = 0
    out = []
    for ch in text:
        if ch.isalpha():
            k = ord(key[j % len(key)]) - 65
            j += 1
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base - k) % 26 + base))
        else:
            out.append(ch if ch in SYMBOLS else ch)
    return ''.join(out)
