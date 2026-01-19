from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class Note:
    title: str
    tags: List[str]
    cipher: str
    params: Dict[str, Any]
    ciphertext_b64: str
    created_at: str
