import json, base64, os, glob, time
from typing import List, Dict
from store.model import Note

NOTES_DIR = "data/notes"

def b64e(s: str) -> str: return base64.b64encode(s.encode("utf-8")).decode("ascii")
def b64d(s: str) -> str: return base64.b64decode(s.encode("ascii")).decode("utf-8")

def _path(title: str) -> str:
    safe = "".join(ch for ch in title if ch.isalnum() or ch in "-_ ")
    return os.path.join(NOTES_DIR, f"{safe}.enc.json")

def save_note(note: Note) -> None:
    os.makedirs(NOTES_DIR, exist_ok=True)
    with open(_path(note.title), "w", encoding="utf-8") as f:
        json.dump(note._dict_, f, ensure_ascii=False, indent=2)

def load_note(title: str) -> Note | None:
    p = _path(title)
    if not os.path.exists(p): return None
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    return Note(**d)

def list_titles() -> List[str]:
    os.makedirs(NOTES_DIR, exist_ok=True)
    out = []
    for p in glob.glob(os.path.join(NOTES_DIR, "*.enc.json")):
        out.append(os.path.splitext(os.path.basename(p))[0])
    return sorted(out)

def search_by_tag(tag: str) -> List[str]:
    tag = tag.lower()
    hits = []
    for t in list_titles():
        n = load_note(t)
        if any(tag in x.lower() for x in n.tags):
            hits.append(t)
    return hits
