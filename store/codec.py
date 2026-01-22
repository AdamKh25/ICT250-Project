import json, os, base64, re
from datetime import datetime
from typing import Dict, Any
from store.model import Note


# return current utc time in iso format
def now_iso_utc() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


# base64 encode text
def b64e(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


# base64 decode text
def b64d(data: str) -> str:
    return base64.b64decode(data.encode("ascii")).decode("utf-8")


# create safe filename from title
def _safe_filename(name: str) -> str:
    # remove unsupported characters
    return re.sub(r"[^A-Za-z0-9 -]+", "", name).strip() or "note"


# convert note object to dictionary
def note_to_dict(n: Note) -> Dict[str, Any]:
    return {
        "title": n.title,
        "tags": n.tags,
        "cipher": n.cipher,
        "params": n.params,
        "ciphertext_b64": n.ciphertext_b64,
        "created_at": n.created_at,
    }


# convert dictionary to note object
def dict_to_note(d: Dict[str, Any]) -> Note:
    return Note(
        title=d["title"],
        tags=list(d.get("tags", [])),
        cipher=str(d["cipher"]),
        params=dict(d.get("params", {})),
        ciphertext_b64=str(d["ciphertext_b64"]),
        created_at=str(d.get("created_at", now_iso_utc())),
    )


# save encrypted note to file
def save_note(path: str, note: Note) -> None:
    # create directory if missing
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # write note data as json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(note_to_dict(note), f, ensure_ascii=False, indent=2)


# load encrypted note from file
def load_note(path: str) -> Note:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return dict_to_note(data)


# build full file path for a note
def build_note_path(base_dir: str, title: str) -> str:
    fname = _safe_filename(title) + ".enc.json"
    return os.path.join(base_dir, fname)
