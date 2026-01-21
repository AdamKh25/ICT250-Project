LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = 26

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def modInverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def getKeyParts(key):
    keyA = key // M
    keyB = key % M
    return keyA, keyB

def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    if gcd(keyA, M) != 1:
        raise ValueError('Key A and 26 are not relatively prime.')
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            num = (keyA * num + keyB) % M
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    invA = modInverse(keyA, M)
    if invA is None:
        raise ValueError('Key A has no inverse mod 26.')
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            num = (invA * (num - keyB)) % M
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def encrypt(text, key): return encryptMessage(key, text)
def decrypt(text, key): return decryptMessage(key, text)
