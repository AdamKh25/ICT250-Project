# supported characters for the cipher
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


# encrypt text using shift over symbols
def encrypt(text: str, key: int) -> str:
    result = []

    # process each character
    for ch in text:
        if ch in SYMBOLS:
            # get character index
            idx = SYMBOLS.index(ch)

            # shift index forward by key
            new_idx = (idx + key) % len(SYMBOLS)

            # append encrypted character
            result.append(SYMBOLS[new_idx])
        else:
            # keep unsupported characters unchanged
            result.append(ch)

    # return encrypted string
    return ''.join(result)


# decrypt text using reverse shift
def decrypt(text: str, key: int) -> str:
    result = []

    # process each character
    for ch in text:
        if ch in SYMBOLS:
            # get character index
            idx = SYMBOLS.index(ch)

            # shift index backward by key
            new_idx = (idx - key) % len(SYMBOLS)

            # append decrypted character
            result.append(SYMBOLS[new_idx])
        else:
            # keep unsupported characters unchanged
            result.append(ch)

    # return decrypted string
    return ''.join(result)
