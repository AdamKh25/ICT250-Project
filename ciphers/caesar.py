SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def encrypt(text: str, key: int) -> str:
    result = []
    for ch in text:
        if ch in SYMBOLS:
            idx = SYMBOLS.index(ch)
            new_idx = (idx + key) % len(SYMBOLS)
            result.append(SYMBOLS[new_idx])
        else:
            # if not in SYMBOLS, leave as-is (like slides often suggest)
            result.append(ch)
    return ''.join(result)

def decrypt(text: str, key: int) -> str:
    result = []
    for ch in text:
        if ch in SYMBOLS:
            idx = SYMBOLS.index(ch)
            new_idx = (idx - key) % len(SYMBOLS)
            result.append(SYMBOLS[new_idx])
        else:
            result.append(ch)
    return ''.join(result)
