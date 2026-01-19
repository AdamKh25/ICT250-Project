from validation import require_text
from typing import Tuple

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def prepare_key(key: str, text_len: int) -> str:
    """Repeat key to match text length."""
    key = ''.join(c for c in key.upper() if c in SYMBOLS[:26])
    return (key * (text_len // len(key) + 1))[:text_len]

def encrypt(text: str, key: str) -> str:
    require_text('text', text
