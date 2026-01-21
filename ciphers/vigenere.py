LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encryptMessage(key, message):
    key = key.upper()
    translated = []
    keyIndex = 0
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            k   = LETTERS.find(key[keyIndex])
            num = (num + k) % 26
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
            keyIndex = (keyIndex + 1) % len(key)
        else:
            translated.append(symbol)
    return ''.join(translated)

def decryptMessage(key, message):
    key = key.upper()
    translated = []
    keyIndex = 0
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            k   = LETTERS.find(key[keyIndex])
            num = (num - k) % 26
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
            keyIndex = (keyIndex + 1) % len(key)
        else:
            translated.append(symbol)
    return ''.join(translated)

def encrypt(text, key): return encryptMessage(key, text)
def decrypt(text, key): return decryptMessage(key, text)
