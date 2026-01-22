import os, json
from typing import List, Dict, Any
from store.model import Note
from store.codec import dict_to_note


# check if filename matches note format
def _is_note_file(name: str) -> bool:
    # notes are saved as .enc.json files
    return name.endswith(".enc.json")


# search notes that contain all required tags
def search_by_tags(folder: str, required_tags: List[str]) -> List[Note]:
    # normalize required tags
    required = [t.strip().lower() for t in required_tags if t.strip()]

    found: List[Note] = []

    # return empty list if folder does not exist
    if not os.path.isdir(folder):
        return found

    # scan files in folder
    for name in os.listdir(folder):
        if not _is_note_file(name):
            continue

        path = os.path.join(folder, name)

        try:
            # load note json
            with open(path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)

            # normalize stored tags
            tags = [str(t).lower() for t in data.get("tags", [])]

            # check if all required tags exist
            ok = all(t in tags for t in required)

            if ok:
                found.append(dict_to_note(data))

        except Exception:
            # skip invalid or corrupted files
            continue

    return found
