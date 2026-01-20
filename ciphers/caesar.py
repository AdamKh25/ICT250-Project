from validation import SYMBOLS

def encrypt(text: str, key: int) -> str:
    key %= 26
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - 65 + key) % 26 + 65))
        elif 'a' <= ch <= 'z':
            out.append(chr((ord(ch) - 97 + key) % 26 + 97))
        else:
            # non-letters are left as-is (rule: keep unchanged)
            out.append(ch if ch in SYMBOLS else ch)
    return ''.join(out)

def decrypt(text: str, key: int) -> str:
    return encrypt(text, -key)
