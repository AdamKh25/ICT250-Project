from dataclasses import dataclass
from typing import List, Dict
@dataclass
class Note:
    title: str
    tags: List[str]
    cipher: str                   
    params: Dict[str, str | int]   
    ciphertext_b64: str            
    created_at: str                
