from validation import require_text, require_int, is_valid_affine_a, make_affine_key

# Optional imports (guarded so main still runs if a file is missing)
def _try_import(path):
    try:
        mod = __import__(path, fromlist=["*"])
        return mod
    except Exception:
        return None

caesar = _try_import("ciphers.caesar")
vigenere = _try_import("ciphers.vigenere")
affine = _try_import("ciphers.affine")
transposition = _try_import("ciphers.transposition")

cz_hack = _try_import("hacking.caesar_hack")
af_hack = _try_import("hacking.affine_hack")

def _pick(prompt, choices):
    print(prompt)
    for i, label in enumerate(choices, 1):
        print(f"{i}) {label}")
    n = input("> ").strip()
    try:
        n = int(n)
        if 1 <= n <= len(choices): return n
    except Exception:
        pass
    print("Invalid choice.")
    return None

def action_encrypt():
    n = _pick("Choose cipher to ENCRYPT:", [
        "Caesar", "Vigenere", "Affine", "Transposition"
    ])
    if not n: return
    text = require_text(input("Plaintext: "))
    if n == 1:
        if not caesar: return print("Caesar not available.")
        key = require_int(input("Key (int): "))
        print("Ciphertext:", caesar.encrypt(text, key))
    elif n == 2:
        if not vigenere: return print("Vigenere not available.")
        key = require_text(input("Key (letters): "))
        print("Ciphertext:", vigenere.encrypt(text, key))
    elif n == 3:
        if not affine: return print("Affine not available.")
        a = require_int(input("a (coprime with 26): "))
        b = require_int(input("b (0..25): "))
        if not is_valid_affine_a(a):
            return print("Invalid a: gcd(a,26) must be 1.")
        key = make_affine_key(a, b)
        print("Ciphertext:", affine.encrypt(text, key))
    elif n == 4:
        if not transposition: return print("Transposition not available.")
        key = require_int(input("Key (int >= 2): "))
        if key < 2: return print("Key must be >= 2.")
        print("Ciphertext:", transposition.encrypt(text, key))

def action_decrypt():
    n = _pick("Choose cipher to DECRYPT:", [
        "Caesar", "Vigenere", "Affine", "Transposition"
    ])
    if not n: return
    ct = require_text(input("Ciphertext: "))
    if n == 1:
        if not caesar: return print("Caesar not available.")
        key = require_int(input("Key (int): "))
        print("Plaintext:", caesar.decrypt(ct, key))
    elif n == 2:
        if not vigenere: return print("Vigenere not available.")
        key = require_text(input("Key (letters): "))
        print("Plaintext:", vigenere.decrypt(ct, key))
    elif n == 3:
        if not affine: return print("Affine not available.")
        a = require_int(input("a (coprime with 26): "))
        b = require_int(input("b (0..25): "))
        if not is_valid_affine_a(a):
            return print("Invalid a: gcd(a,26) must be 1.")
        key = make_affine_key(a, b)
        print("Plaintext:", affine.decrypt(ct, key))
    elif n == 4:
        if not transposition: return print("Transposition not available.")
        key = require_int(input("Key (int >= 2): "))
        if key < 2: return print("Key must be >= 2.")
        print("Plaintext:", transposition.decrypt(ct, key))

def action_hack():
    n = _pick("Choose hack:", [
        "Brute-force Caesar", "Brute-force Affine"
    ])
    if not n: return
    ct = require_text(input("Ciphertext to hack: "))
    if n == 1:
        if not cz_hack: return print("Caesar hack not available.")
        pt, key, top = cz_hack.hack(ct)
        print(f"Best: key={key}  -> {pt}")
        for s, k, cand in top:
            print(f"{s:.3f}  key={k}  {cand[:60]}")
    elif n == 2:
        if not af_hack: return print("Affine hack not available.")
        pt, (a, b), top = af_hack.hack(ct)
        print(f"Best: a={a}, b={b}  -> {pt}")
        for s, (aa, bb), cand in top:
            print(f"{s:.3f}  a={aa}, b={bb}  {cand[:60]}")

def main():
    while True:
        n = _pick("Secure Notes Vault - Demo CLI", [
            "Encrypt", "Decrypt", "Hack (Caesar/Affine)", "Quit"
        ])
        if n == 1: action_encrypt()
        elif n == 2: action_decrypt()
        elif n == 3: action_hack()
        elif n == 4 or n is None:
            print("Bye."); break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
