# alphabet used for substitution cipher
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# check if substitution key is valid
def checkValidKey(key):
    key = key.upper()
    # key must contain all 26 letters exactly once
    return len(key) == 26 and sorted(key) == sorted(LETTERS)


# encrypt message using substitution cipher
def encryptMessage(key, message):
    key = key.upper()
    translated = []

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # find letter index
            idx = LETTERS.find(symbol.upper())

            # substitute using key
            new = key[idx]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())
        else:
            # keep non-letters unchanged
            translated.append(symbol)

    return ''.join(translated)


# decrypt message using substitution cipher
def decryptMessage(key, message):
    key = key.upper()
    translated = []

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # find index in key
            idx = key.find(symbol.upper())

            # map back to original letter
            new = LETTERS[idx]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())
        else:
            # keep non-letters unchanged
            translated.append(symbol)

    return ''.join(translated)


# wrapper for encryption
def encrypt(text, key): 
    # validate key before encrypting
    if not checkValidKey(key):
        raise ValueError("Invalid substitution key.")
    return encryptMessage(key, text)


# wrapper for decryption
def decrypt(text, key): 
    # validate key before decrypting
    if not checkValidKey(key):
        raise ValueError("Invalid substitution key.")
    return decryptMessage(key, text)
