import secrets

# alphabet used for otp
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# keep only letters and convert to uppercase
def onlyLettersUp(s): 
    return ''.join(ch for ch in s.upper() if ch in LETTERS)


# generate random key matching number of letters in message
def makeRandomKeyFor(message):
    # count letters in message
    L = sum(1 for ch in message if ch.upper() in LETTERS)
    # generate random letters
    return ''.join(secrets.choice(LETTERS) for _ in range(L))


# shift single character using otp logic
def _shift(ch, k, enc=True):
    # get letter positions
    a = LETTERS.find(ch.upper())
    b = LETTERS.find(k)

    # apply shift or reverse shift
    n = (a + b) % 26 if enc else (a - b) % 26
    out = LETTERS[n]

    # keep original case
    return out if ch.isupper() else out.lower()


# encrypt message using otp
def encryptMessage(message, key):
    # normalize key
    key = onlyLettersUp(key)
    out, i = [], 0

    # process each character
    for ch in message:
        if ch.upper() in LETTERS:
            out.append(_shift(ch, key[i], True))
            i += 1
        else:
            # keep non-letters unchanged
            out.append(ch)

    return ''.join(out)


# decrypt message using otp
def decryptMessage(message, key):
    # normalize key
    key = onlyLettersUp(key)
    out, i = [], 0

    # process each character
    for ch in message:
        if ch.upper() in LETTERS:
            out.append(_shift(ch, key[i], False))
            i += 1
        else:
            # keep non-letters unchanged
            out.append(ch)

    return ''.join(out)


# generate random otp key of given length
def generate_key(length): 
    return ''.join(secrets.choice(LETTERS) for _ in range(length))


# encrypt wrapper used by project
def encrypt(text, key=None):
    # generate key if not provided
    if key is None:
        key = makeRandomKeyFor(text)

    # ensure key length matches number of letters
    if sum(1 for c in text if c.upper() in LETTERS) != len(onlyLettersUp(key)):
        raise ValueError("OTP key length must equal number of letters in message.")

    return encryptMessage(text, key), key


# decrypt wrapper used by project
def decrypt(ciphertext, key):
    return decryptMessage(ciphertext, key)
