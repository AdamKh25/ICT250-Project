from validation import require_text

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
UPPER = SYMBOLS[:26]

def validate_key(key: str):
    require_text('key', key)
    if len(key) != 26 or len(set(key)) != 26 or not key.isupper():
        raise ValueError("26 unique uppercase A-Z")

def encrypt(text: str, key: str) -> str:
    validate_key(key)
    mapping = str.maketrans(UPPER, key)
    return text.translate(mapping)

def decrypt(ct: str, key: str) -> str:
    validate_key(key)
    inv = str.maketrans(key, UPPER)
    return ct.translate(inv)

if __name__ == "__main__":
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    ct = encrypt("HELLO", key)
    print(decrypt(ct, key) == "HELLO")
