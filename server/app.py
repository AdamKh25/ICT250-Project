# server/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys

# Make `ciphers/`, `hacking/`, and `store/` importable when running from /server
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --- local modules (your course-style implementations) ---
from ciphers import caesar, vigenere, affine, transposition
from hacking import caesar_hack, affine_hack
from store.codec import save_note, load_note, list_titles, search_by_tag

app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return "ok", 200

# -------- encrypt / decrypt ----------
@app.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    p      = data.get("params") or {}

    try:
        if cipher == "caesar":
            out = caesar.encrypt(text, int(p.get("key", 0)))
        elif cipher == "vigenere":
            out = vigenere.encrypt(text, str(p.get("key","")))
        elif cipher == "affine":
            out = affine.encrypt(text, int(p.get("key")))
        elif cipher == "transposition":
            out = transposition.encrypt(text, int(p.get("key", 0)))
        else:
            return jsonify(ok=False, error="Unknown cipher"), 400
        return jsonify(ok=True, ciphertext=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400

@app.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    p      = data.get("params") or {}

    try:
        if cipher == "caesar":
            out = caesar.decrypt(text, int(p.get("key", 0)))
        elif cipher == "vigenere":
            out = vigenere.decrypt(text, str(p.get("key","")))
        elif cipher == "affine":
            out = affine.decrypt(text, int(p.get("key")))
        elif cipher == "transposition":
            out = transposition.decrypt(text, int(p.get("key", 0)))
        else:
            return jsonify(ok=False, error="Unknown cipher"), 400
        return jsonify(ok=True, plaintext=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400

# -------- hack endpoints (this is what was 404) ----------
@app.post("/api/hack/caesar")
def api_hack_caesar():
    data = request.get_json(force=True)
    ct = data.get("ciphertext") or data.get("text") or ""
    best, key, candidates = caesar_hack.hack(ct)
    return jsonify(ok=True, plaintext=best, key=key, candidates=candidates[:10])

@app.post("/api/hack/affine")
def api_hack_affine():
    data = request.get_json(force=True)
    ct = data.get("ciphertext") or data.get("text") or ""
    best, (a,b), candidates = affine_hack.hack(ct)
    return jsonify(ok=True, plaintext=best, a=a, b=b, candidates=candidates[:10])

# -------- notes (save/list/open/search) ----------
@app.post("/api/note/save")
def api_note_save():
    data = request.get_json(force=True)
    title  = data["title"]
    tags   = data.get("tags", [])
    cipher = data["cipher"]
    params = data.get("params", {})
    pt     = data["plaintext"]

    # encrypt via same functions above
    if cipher.lower() == "caesar":
        ct = caesar.encrypt(pt, int(params.get("key", 0)))
    elif cipher.lower() == "vigenere":
        ct = vigenere.encrypt(pt, str(params.get("key","")))
    elif cipher.lower() == "affine":
        ct = affine.encrypt(pt, int(params.get("key")))
    elif cipher.lower() == "transposition":
        ct = transposition.encrypt(pt, int(params.get("key", 0)))
    else:
        return jsonify(ok=False, error="Unknown cipher"), 400

    save_note(title, tags, cipher, params, ct)
    return jsonify(ok=True)

@app.get("/api/note/list")
def api_note_list():
    return jsonify(ok=True, titles=list_titles())

@app.get("/api/note/open")
def api_note_open():
    title = request.args.get("title","")
    note  = load_note(title)
    if not note:
        return jsonify(ok=False, error="not found"), 404
    return jsonify(ok=True, note=note)

@app.get("/api/note/search")
def api_note_search():
    tag = request.args.get("tag","")
    return jsonify(ok=True, titles=search_by_tag(tag))

if __name__ == "__main__":
    # Run Flask dev server on 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
