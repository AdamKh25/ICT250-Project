
import os, json
from typing import List, Dict, Any
from store.model import Note
from store.codec import dict_to_note

def _is_note_file(name: str) -> bool:
    # We save notes as *.enc.json
    return name.endswith(".enc.json")

def search_by_tags(folder: str, required_tags: List[str]) -> List[Note]:
    """
    Return notes whose 'tags' contain ALL tags in required_tags.
    """
    required = [t.strip().lower() for t in required_tags if t.strip()]
    found: List[Note] = []

    if not os.path.isdir(folder):
        return found

    for name in os.listdir(folder):
        if not _is_note_file(name):
            continue
        path = os.path.join(folder, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
            tags = [str(t).lower() for t in data.get("tags", [])]
            ok = all(t in tags for t in required)
            if ok:
                found.append(dict_to_note(data))
        except Exception:
            # Skip broken files quietly (beginner-friendly)
            continue
    return found
