LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(text: str, key: int) -> str:
    text = text.upper()
    result = ''

    for symbol in text:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = (num + key) % len(LETTERS)
            result += LETTERS[num]
        else:
            # keep spaces, commas, etc.
            result += symbol

    return result

def decrypt(text: str, key: int) -> str:
    text = text.upper()
    result = ''

    for symbol in text:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = (num - key) % len(LETTERS)
            result += LETTERS[num]
        else:
            result += symbol

    return result
