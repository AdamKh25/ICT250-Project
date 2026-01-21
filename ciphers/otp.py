import secrets
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def onlyLettersUp(s): 
    return ''.join(ch for ch in s.upper() if ch in LETTERS)

def makeRandomKeyFor(message):
    # random letters only for the letters in message
    L = sum(1 for ch in message if ch.upper() in LETTERS)
    return ''.join(secrets.choice(LETTERS) for _ in range(L))

def _shift(ch, k, enc=True):
    a = LETTERS.find(ch.upper())
    b = LETTERS.find(k)
    n = (a + b) % 26 if enc else (a - b) % 26
    out = LETTERS[n]
    return out if ch.isupper() else out.lower()

def encryptMessage(message, key):
    key = onlyLettersUp(key)
    out, i = [], 0
    for ch in message:
        if ch.upper() in LETTERS:
            out.append(_shift(ch, key[i], True))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)

def decryptMessage(message, key):
    key = onlyLettersUp(key)
    out, i = [], 0
    for ch in message:
        if ch.upper() in LETTERS:
            out.append(_shift(ch, key[i], False))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)

# project adapters (encrypt returns (cipher, key) if key missing)
def generate_key(length): 
    return ''.join(secrets.choice(LETTERS) for _ in range(length))

def encrypt(text, key=None):
    if key is None:
        key = makeRandomKeyFor(text)
    # strict: key letters count must equal text letters count
    if sum(1 for c in text if c.upper() in LETTERS) != len(onlyLettersUp(key)):
        raise ValueError("OTP key length must equal number of letters in message.")
    return encryptMessage(text, key), key

def decrypt(ciphertext, key):
    return decryptMessage(ciphertext, key)
