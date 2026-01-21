# main.py
from datetime import datetime
from store.model import Note
from store.codec import b64e, b64d, save_note, load_note, build_note_path, now_iso_utc
from store.search import search_by_tags

# Slide-style ciphers/hacks
from ciphers import caesar, vigenere, affine, transposition
from hacking import caesar_hack, affine_hack

def line():
    print("-" * 60)

def menu():
    print("\nSecure Notes Vault — CLI")
    line()
    print("1) Encrypt")
    print("2) Decrypt")
    print("3) Hack (Caesar)")
    print("4) Hack (Affine)")
    print("5) Save note to data/notes")
    print("6) Search notes by tag")
    print("0) Exit")
    return input("Choose: ").strip()

def encrypt_flow():
    print("\nEncrypt")
    cipher = input("Cipher [caesar|vigenere|affine|transposition]: ").strip().lower()
    text   = input("Plaintext: ")
    if cipher == "caesar":
        key = int(input("Key (int): "))
        ct  = caesar.encrypt(text, key)
    elif cipher == "vigenere":
        key = input("Keyword (letters): ")
        ct  = vigenere.encrypt(text, key)
    elif cipher == "affine":
        a   = int(input("a (coprime with 26): "))
        b   = int(input("b (0..25): "))
        key = a * 26 + (b % 26)
        ct  = affine.encrypt(text, key)
    elif cipher == "transposition":
        key = int(input("Key (int >= 2): "))
        ct  = transposition.encrypt(text, key)
    else:
        print("Unknown cipher.")
        return
    print("Ciphertext:", ct)

def decrypt_flow():
    print("\nDecrypt")
    cipher = input("Cipher [caesar|vigenere|affine|transposition]: ").strip().lower()
    text   = input("Ciphertext: ")
    if cipher == "caesar":
        key = int(input("Key (int): "))
        pt  = caesar.decrypt(text, key)
    elif cipher == "vigenere":
        key = input("Keyword (letters): ")
        pt  = vigenere.decrypt(text, key)
    elif cipher == "affine":
        a   = int(input("a (coprime with 26): "))
        b   = int(input("b (0..25): "))
        key = a * 26 + (b % 26)
        pt  = affine.decrypt(text, key)
    elif cipher == "transposition":
        key = int(input("Key (int >= 2): "))
        pt  = transposition.decrypt(text, key)
    else:
        print("Unknown cipher.")
        return
    print("Plaintext:", pt)

def hack_caesar_flow():
    print("\nHack — Caesar")
    ct = input("Ciphertext: ")
    pt, key, top = caesar_hack.hack(ct)
    print(f"Best plaintext: {pt}")
    print(f"Key: {key}")
    print("Top tries:")
    for score, k, cand in top:
        print(f"  k={k} score={score:.2f}  {cand}")

def hack_affine_flow():
    print("\nHack — Affine")
    ct = input("Ciphertext: ")
    pt, (a, b), top = affine_hack.hack(ct)
    print(f"Best plaintext: {pt}")
    print(f"a={a}, b={b}")
    print("Top tries:")
    for score, (aa, bb), cand in top:
        print(f"  a={aa} b={bb} score={score:.2f}  {cand}")

def save_note_flow():
    print("\nSave Note")
    title  = input("Title: ").strip()
    tags   = [t.strip() for t in input("Tags (comma separated): ").split(",") if t.strip()]
    cipher = input("Cipher used [caesar|vigenere|affine|transposition]: ").strip().lower()
    ct     = input("Ciphertext: ")

    params = {}
    if cipher == "caesar":
        params["key"] = input("Store key (int) or leave blank: ").strip()
    elif cipher == "vigenere":
        params["key"] = input("Store keyword or leave blank: ").strip()
    elif cipher == "affine":
        a = input("Store a (optional): ").strip()
        b = input("Store b (optional): ").strip()
        if a: params["a"] = a
        if b: params["b"] = b
    elif cipher == "transposition":
        params["key"] = input("Store key (int) or leave blank: ").strip()

    n = Note(
        title=title,
        tags=tags,
        cipher=cipher,
        params=params,
        ciphertext_b64=b64e(ct),
        created_at=now_iso_utc(),
    )
    path = build_note_path("data/notes", title)
    save_note(path, n)
    print(f"Saved: {path}")

def search_flow():
    print("\nSearch Notes by Tag")
    tag = input("Tag (single): ").strip()
    hits = search_by_tags("data/notes", [tag])
    if not hits:
        print("No matches.")
        return
    print(f"Found {len(hits)} note(s):")
    for i, n in enumerate(hits, 1):
        print(f"{i}. {n.title}  tags={n.tags}  cipher={n.cipher}  created={n.created_at}")

def main():
    print("Welcome!")
    while True:
        choice = menu()
        if choice == "1":
            encrypt_flow()
        elif choice == "2":
            decrypt_flow()
        elif choice == "3":
            hack_caesar_flow()
        elif choice == "4":
            hack_affine_flow()
        elif choice == "5":
            save_note_flow()
        elif choice == "6":
            search_flow()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
