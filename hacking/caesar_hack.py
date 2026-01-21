LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decryptWithKey(message, key):
    # Classic Caesar decryption used in slides
    translated = []
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            num = (num - key) % 26
            new = LETTERS[num]
            translated.append(new if symbol.isupper() else new.lower())
        else:
            translated.append(symbol)
    return ''.join(translated)

def englishScore(s):
    # Simple slide-like “detect English” stand-in
    s = s.upper()
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ']
    return (
        sum(s.count(w) for w in common) * 3
        + s.count(' ')
        + 0.02 * sum(ch.isalpha() for ch in s)
    )

def hackCaesar(ciphertext):
    # Slide-like loop over 0..25, keep best plaintext
    bestScore = float('-inf')
    bestKey = 0
    bestText = ciphertext
    tries = []
    for key in range(26):
        pt = decryptWithKey(ciphertext, key)
        score = englishScore(pt)
        tries.append((score, key, pt))
        if score > bestScore:
            bestScore, bestKey, bestText = score, key, pt
    tries.sort(reverse=True)
    return bestText, bestKey, tries[:3]

# keep your project’s entry point name
def hack(ciphertext):
    return hackCaesar(ciphertext)
