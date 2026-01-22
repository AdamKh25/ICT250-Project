# alphabet used for vigenere cipher
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# encrypt message using vigenere cipher
def encryptMessage(key, message):
    # normalize key
    key = key.upper()
    translated = []
    keyIndex = 0

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # get plaintext letter index
            num = LETTERS.find(symbol.upper())

            # get key letter index
            k = LETTERS.find(key[keyIndex])

            # apply vigenere shift
            num = (num + k) % 26
            new = LETTERS[num]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())

            # move to next key character
            keyIndex = (keyIndex + 1) % len(key)
        else:
            # keep non-letters unchanged
            translated.append(symbol)

    return ''.join(translated)


# decrypt message using vigenere cipher
def decryptMessage(key, message):
    # normalize key
    key = key.upper()
    translated = []
    keyIndex = 0

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # get ciphertext letter index
            num = LETTERS.find(symbol.upper())

            # get key letter index
            k = LETTERS.find(key[keyIndex])

            # apply reverse vigenere shift
            num = (num - k) % 26
            new = LETTERS[num]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())

            # move to next key character
            keyIndex = (keyIndex + 1) % len(key)
        else:
            # keep non-letters unchanged
            translated.append(symbol)

    return ''.join(translated)


# wrapper for encryption
def encrypt(text, key):
    return encryptMessage(key, text)

# wrapper for decryption
def decrypt(text, key):
    return decryptMessage(key, text)
