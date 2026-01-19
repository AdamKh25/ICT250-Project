import os, json, base64
from validation import require_text, require_int
from store.model import Note  # M3
from store.codec import save_note, load_note  # M3
NOTES_DIR = os.path.join("data", "notes")
os.makedirs(NOTES_DIR, exist_ok=True)

def menu_choice(prompt: str, valid: list[str]) -> str:
    while True:
        try:
            choice = require_text("choice", input(prompt).strip())
            if choice in valid: return choice
        except ValueError as e:
            print(f"Error: {e}")

def new_note():
    try:
        title = require_text("title", input("Title: "))
        tags = input("Tags (comma sep): ").split(',')
        text = require_text("text", input("Text: "))
        cipher = menu_choice("Cipher (caesar/vigenere): ", ['caesar', 'vigenere'])
        key = input("Key: ")
        if cipher == 'caesar':
            from ciphers.caesar import encrypt
            ct = encrypt(text, key)
        else:
            from ciphers.vigenere
