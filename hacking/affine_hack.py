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

def decryptAffine(ciphertext, keyA, keyB):
    invA = modInverse(keyA, M)
    if invA is None:
        return None
    translated = []
    for symbol in ciphertext:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            num = (invA * (num - keyB)) % M
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def englishScore(s):
    s = s.upper()
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ']
    return (
        sum(s.count(w) for w in common) * 3
        + s.count(' ')
        + 0.02 * sum(ch.isalpha() for ch in s)
    )

def hackAffine(ciphertext):
    # Slide-like: try all valid keyA with gcd(keyA,26)==1 and keyB in 0..25
    validA = [a for a in range(1, 26, 2) if gcd(a, M) == 1]
    bestScore = float('-inf')
    bestA, bestB = 1, 0
    bestText = ciphertext
    tries = []
    for a in validA:
        for b in range(26):
            pt = decryptAffine(ciphertext, a, b)
            if pt is None:
                continue
            score = englishScore(pt)
            tries.append((score, (a, b), pt))
            if score > bestScore:
                bestScore, bestA, bestB, bestText = score, a, b, pt
    tries.sort(reverse=True)
    return bestText, (bestA, bestB), tries[:3]

# keep your project’s entry point name
def hack(ciphertext):
    return hackAffine(ciphertext)
