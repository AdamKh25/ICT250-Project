from dataclasses import dataclass
from typing import List, Dict


# data class representing an encrypted note
@dataclass
class Note:
    title: str              # note title
    tags: List[str]         # list of tags
    cipher: str             # cipher used
    params: Dict[str, str]  # cipher parameters
    ciphertext_b64: str     # base64 encoded ciphertext
    created_at: str         # creation timestamp
