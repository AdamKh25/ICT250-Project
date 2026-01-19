LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(text: str, key: int) -> str:
    text = text.upper()
    key %= 26
    result = ''
    for ch in text:
        if ch in LETTERS:
            idx = LETTERS.find(ch)
            result += LETTERS[(idx + key) % 26]
        else:
            result += ch
    return result

def decrypt(text: str, key: int) -> str:
    return encrypt(text, -key)
