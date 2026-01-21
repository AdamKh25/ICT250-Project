LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encryptMessage(key, message):
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            num = (num + key) % 26
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def decryptMessage(key, message):
    return encryptMessage(-key, message)

# keep these names for your tests / API
def encrypt(text, key): return encryptMessage(key, text)
def decrypt(text, key): return decryptMessage(key, text)
