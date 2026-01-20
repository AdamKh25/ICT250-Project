import os
from typing import List, Optional
from .codec import load_note
from .model import Note

def search_notes_by_tags(notes_dir: str, tags: List[str]) -> List[Note]:
    tags_lower = [t.strip().lower() for t in tags if t.strip()]
    if not tags_lower:
        return []

    results: List[Note] = []
    if not os.path.isdir(notes_dir):
        return results

    for name in os.listdir(notes_dir):
        if not name.endswith(".enc"):
            continue
        path = os.path.join(notes_dir, name)
        try:
            note = load_note(path)
            note_tags = [t.lower() for t in (note.tags or [])]
            if all(t in note_tags for t in tags_lower):
                results.append(note)
        except Exception:
            continue

    return results

