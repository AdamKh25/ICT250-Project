from validation import require_text
import secrets

def text_to_bytes(text):
    return ''.join(c for c in text if c in SYMBOLS).encode()

def encrypt(text: str, key: bytes = None) -> tuple[str, bytes]:
    ptb = text_to_bytes(text)
    if key is None:
        key = secrets.token_bytes(len(ptb))
    elif len(key) != len(ptb):
        raise ValueError("key len == text len")
    ctb = bytes(a^b for a,b in zip(ptb, key))
    return ctb.decode(errors='ignore'), key

def decrypt(ct: str, key: bytes) -> str:
    ctb = ct.encode(errors='ignore')
    ptb = bytes(a^b for a,b in zip(ctb, key))
    return ptb.decode(errors='ignore')

if __name__ == "__main__":
    ct, k = encrypt("OTPTEST")
    print(decrypt(ct, k))
