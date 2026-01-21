import json, os, base64, re
from datetime import datetime
from typing import Dict, Any
from store.model import Note

def now_iso_utc() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def b64e(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")

def b64d(data: str) -> str:
    return base64.b64decode(data.encode("ascii")).decode("utf-8")

def _safe_filename(name: str) -> str:
    # Keep letters, numbers, space, dash, underscore; replace others with "_"
    return re.sub(r"[^A-Za-z0-9 -]+", "", name).strip() or "note"

def note_to_dict(n: Note) -> Dict[str, Any]:
    return {
        "title": n.title,
        "tags": n.tags,
        "cipher": n.cipher,
        "params": n.params,
        "ciphertext_b64": n.ciphertext_b64,
        "created_at": n.created_at,
    }

def dict_to_note(d: Dict[str, Any]) -> Note:
    return Note(
        title=d["title"],
        tags=list(d.get("tags", [])),
        cipher=str(d["cipher"]),
        params=dict(d.get("params", {})),
        ciphertext_b64=str(d["ciphertext_b64"]),
        created_at=str(d.get("created_at", now_iso_utc())),
    )

def save_note(path: str, note: Note) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(note_to_dict(note), f, ensure_ascii=False, indent=2)

def load_note(path: str) -> Note:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return dict_to_note(data)

def build_note_path(base_dir: str, title: str) -> str:
    # Example: base_dir="data/notes" -> "data/notes/My Secret.enc.json"
    fname = _safe_filename(title) + ".enc.json"
    return os.path.join(base_dir, fname)


