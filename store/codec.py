import json
import base64
from typing import Any, Dict
from .model import Note

def b64e(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")

def b64d(b64: str) -> str:
    return base64.b64decode(b64.encode("ascii")).decode("utf-8")

def note_to_dict(note: Note) -> Dict[str, Any]:
    return {
        "title": note.title,
        "tags": note.tags,
        "cipher": note.cipher,
        "params": note.params,
        "ciphertext_b64": note.ciphertext_b64,
        "created_at": note.created_at,
    }

def dict_to_note(d: Dict[str, Any]) -> Note:
    return Note(
        title=d.get("title", ""),
        tags=list(d.get("tags", [])),
        cipher=d.get("cipher", ""),
        params=dict(d.get("params", {})),
        ciphertext_b64=d.get("ciphertext_b64", ""),
        created_at=d.get("created_at", ""),
    )

def save_note(path: str, note: Note) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(note_to_dict(note), f, ensure_ascii=False, indent=2)

def load_note(path: str) -> Note:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return dict_to_note(data)


