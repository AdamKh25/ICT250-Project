LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(text: str, key: str) -> str:
    text = text.upper()
    key = key.upper()
    result = ''
    j = 0  # index in key for letters only
    for ch in text:
        if ch in LETTERS:
            k = LETTERS.find(key[j % len(key)])
            p = LETTERS.find(ch)
            result += LETTERS[(p + k) % 26]
            j += 1
        else:
            result += ch
    return result

def decrypt(text: str, key: str) -> str:
    text = text.upper()
    key = key.upper()
    result = ''
    j = 0
    for ch in text:
        if ch in LETTERS:
            k = LETTERS.find(key[j % len(key)])
            c = LETTERS.find(ch)
            result += LETTERS[(c - k) % 26]
            j += 1
        else:
            result += ch
    return result
