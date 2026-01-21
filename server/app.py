from flask import Flask, request, jsonify
from flask_cors import CORS
from store.codec import save_note, load_note, list_titles, search_by_tag, b64e, b64d
from store.model import Note
import datetime

app = Flask(__name__)
CORS(app)

def ok(payload): return jsonify({"ok": True, **payload})
def err(msg):    return jsonify({"ok": False, "error": msg}), 400

@app.post("/api/note/save")
def note_save():
    data = request.get_json(force=True)
    title  = str(data.get("title") or "").strip()
    tags   = list(data.get("tags") or [])
    cipher = str(data.get("cipher") or "")
    params = dict(data.get("params") or {})
    text   = str(data.get("plaintext") or "")

    if not title or not cipher:
        return err("title and cipher required")

    # use your existing cipher modules
    try:
        if cipher == "caesar":
            from ciphers import caesar
            ct = caesar.encrypt(text, int(params.get("key", 0)))
        elif cipher == "vigenere":
            from ciphers import vigenere
            ct = vigenere.encrypt(text, str(params.get("key","")))
        elif cipher == "affine":
            from ciphers import affine
            a = int(params.get("a", 5)); b = int(params.get("b", 8))
            ct = affine.encrypt(text, (a*26 + b))
        elif cipher == "transposition":
            from ciphers import transposition
            ct = transposition.encrypt(text, int(params.get("key", 4)))
        else:
            return err("unknown cipher")
    except Exception as e:
        return err(f"encrypt failed: {e}")

    note = Note(
        title=title,
        tags=tags,
        cipher=cipher,
        params=params,
        ciphertext_b64=b64e(ct),
        created_at=datetime.datetime.utcnow().isoformat()+"Z"
    )
    save_note(note)
    return ok({"saved": title})

@app.get("/api/note/open")
def note_open():
    title = request.args.get("title","")
    n = load_note(title)
    if not n: return err("not found")
    return ok({"title": n.title, "tags": n.tags, "cipher": n.cipher,
               "params": n.params, "ciphertext": b64d(n.ciphertext_b64),
               "created_at": n.created_at})

@app.get("/api/note/list")
def note_list():
    return ok({"titles": list_titles()})

@app.get("/api/note/search")
def note_search():
    tag = request.args.get("tag","")
    return ok({"titles": search_by_tag(tag)})
