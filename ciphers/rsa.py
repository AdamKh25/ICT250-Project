def egcd(a,b):
    while b: a,b = b, a%b
    return a

def modInverse(a, m):
    a %= m
    for x in range(1, m):
        if (a*x) % m == 1: return x
    return None

def makeKeys(p, q, e=65537):
    n = p*q
    phi = (p-1)*(q-1)
    if egcd(e, phi) != 1:
        # fallback tiny e
        for cand in (3,5,17,257,65537):
            if egcd(cand, phi) == 1:
                e = cand; break
    d = modInverse(e, phi)
    if d is None: raise ValueError("No inverse for e.")
    return (n, e), (n, d)

def encryptMessage(message, pub):
    n, e = pub
    return [pow(ord(ch), e, n) for ch in message]

def decryptMessage(cipherBlocks, priv):
    n, d = priv
    return ''.join(chr(pow(c, d, n)) for c in cipherBlocks)

# adapters
def encrypt(text, pub): return encryptMessage(text, pub)
def decrypt(blocks, priv): return decryptMessage(blocks, priv)
