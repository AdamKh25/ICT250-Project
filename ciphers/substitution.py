LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def checkValidKey(key):
    key = key.upper()
    return len(key) == 26 and sorted(key) == sorted(LETTERS)

def encryptMessage(key, message):
    key = key.upper()
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            idx = LETTERS.find(symbol.upper())
            new = key[idx]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def decryptMessage(key, message):
    key = key.upper()
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            idx = key.find(symbol.upper())
            new = LETTERS[idx]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

# project adapters
def encrypt(text, key): 
    if not checkValidKey(key): raise ValueError("Invalid substitution key.")
    return encryptMessage(key, text)
def decrypt(text, key): 
    if not checkValidKey(key): raise ValueError("Invalid substitution key.")
    return decryptMessage(key, text)
