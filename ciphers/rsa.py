# compute gcd using euclidean algorithm
def egcd(a, b):
    while b:
        a, b = b, a % b
    return a


# find modular inverse of a mod m
def modInverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# generate rsa public and private keys
def makeKeys(p, q, e=65537):
    # compute modulus
    n = p * q

    # compute totient
    phi = (p - 1) * (q - 1)

    # ensure e is coprime with phi
    if egcd(e, phi) != 1:
        # try smaller fallback values
        for cand in (3, 5, 17, 257, 65537):
            if egcd(cand, phi) == 1:
                e = cand
                break

    # compute private exponent
    d = modInverse(e, phi)
    if d is None:
        raise ValueError("No inverse for e.")

    # return public and private keys
    return (n, e), (n, d)


# encrypt message using rsa public key
def encryptMessage(message, pub):
    n, e = pub
    return [pow(ord(ch), e, n) for ch in message]


# decrypt message using rsa private key
def decryptMessage(cipherBlocks, priv):
    n, d = priv
    return ''.join(chr(pow(c, d, n)) for c in cipherBlocks)


# wrapper for encryption
def encrypt(text, pub):
    return encryptMessage(text, pub)

# wrapper for decryption
def decrypt(blocks, priv):
    return decryptMessage(blocks, priv)
