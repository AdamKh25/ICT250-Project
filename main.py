# main cli entry point
from datetime import datetime
from store.model import Note
from store.codec import b64e, b64d, save_note, load_note, build_note_path, now_iso_utc
from store.search import search_by_tags

# import cipher and hacking modules
from ciphers import caesar, vigenere, affine, transposition
from hacking import caesar_hack, affine_hack


# print separator line
def line():
    print("-" * 60)


# display main menu and get user choice
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


# handle encryption flow
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


# handle decryption flow
def decrypt_flow():
    print("\nDecrypt")
    cipher = input("Cipher [caesar|vigenere|affine|transposition]: ").strip().lower()
    text   = input("Ciphertext: ")

    if cipher == "ca
