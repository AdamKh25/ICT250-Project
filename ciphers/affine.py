# alphabet used for affine cipher
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# alphabet size
M = 26


# compute greatest common divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


# find modular inverse of a mod m
def modInverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# split key into a and b parts
def getKeyParts(key):
    keyA = key // M  # multiplicative part
    keyB = key % M   # additive part
    return keyA, keyB


# encrypt message using affine cipher
def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)

    # check that a is coprime with 26
    if gcd(keyA, M) != 1:
        raise ValueError('Key A and 26 are not relatively prime.')

    translated = []

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # convert letter to number
            num = LETTERS.find(symbol.upper())

            # apply affine formula
            num = (keyA * num + keyB) % M

            # convert back to letter
            new = LETTERS[num]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())
        else:
            # keep non-letters unchanged
            translated.append(symbol)

    return ''.join(translated)


# decrypt message using affine cipher
def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)

    # find inverse of a
    invA = modInverse(keyA, M)
    if invA is None:
        raise ValueError('Key A has no inverse mod 26.')

    translated = []

    # process each character
    for symbol in message:
        if symbol.upper() in LETTERS:
            # convert letter to number
            num = LETTERS.find(symbol.upper())

            # apply inverse affine formula
            num = (invA * (num - keyB)) % M

            # convert back to letter
            new = LETTERS[num]

            # keep original case
            translated.append(new if symbol.isupper() else new.lower())
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
