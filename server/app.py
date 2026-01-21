# server/app.py
import os, sys
# Ensure the project root (the folder that contains ciphers/, store/, web/, server/) is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

# Project imports (will work because of the sys.path append above)
from ciphers import caesar, affine, vigenere, transposition
from store.codec import save_note, load_note, list_titles, search_by_tag

app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return jsonify({"ok": True})

def _encrypt(cipher, text, params):
    if cipher == "caesar":
        key = int(params.get("key", 0))
        return caesar.encrypt(text, key)
    elif cipher == "vigenere":
        key = str(params.get("key", ""))
        return vigenere.encrypt(text, key)
    elif cipher == "affine":
        a = int(params.get("a", 1))
        b = int(params.get("b", 0))
        return affine.encrypt(text, a*26 + b)
    elif cipher == "transposition":
        key = int(params.get("key", 2))
        return transposition.encrypt(text, key)
    else:
        raise ValueError("Unsupported cipher")

def _decrypt(cipher, text, params):
    if cipher == "caesar":
        key = int(params.get("key", 0))
        return caesar.decrypt(text, key)
    elif cipher == "vigenere":
        key = str(params.get("key", ""))
        return vigenere.decrypt(text, key)
    elif cipher == "affine":
        a = int(params.get("a", 1))
        b = int(params.get("b", 0))
        return affine.decrypt(text, a*26 + b)
    elif cipher == "transposition":
        key = int(params.get("key", 2))
        return transposition.decrypt(text, key)
    else:
        raise ValueError("Unsupported cipher")

@app.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(force=True)
    try:
        ct = _encrypt(data["cipher"], data["text"], data.get("params", {}))
        return jsonify({"ok": True, "ciphertext": ct})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(force=True)
    try:
        pt = _decrypt(data["cipher"], data["text"], data.get("params", {}))
        return jsonify({"ok": True, "plaintext": pt})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# --- Notes API (stored on disk) ---
@app.post("/api/note/save")
def api_note_save():
    data = request.get_json(force=True)
    title   = data["title"]
    tags    = data.get("tags", [])
    cipher  = data["cipher"]
    params  = data.get("params", {})
    plaintext = data["plaintext"]
    ciphertext = _encrypt(cipher, plaintext, params)
    save_note(title, tags, cipher, params, ciphertext)
    return jsonify({"ok": True})

@app.get("/api/note/list")
def api_note_list():
    return jsonify({"ok": True, "titles": list_titles()})

@app.get("/api/note/open")
def api_note_open():
    title = request.args.get("title", "")
    note = load_note(title)
    if not note:
        return jsonify({"ok": False, "error": "not found"}), 404
    return jsonify({"ok": True, "note": note})

@app.get("/api/note/search")
def api_note_search():
    tag = request.args.get("tag", "")
    return jsonify({"ok": True, "titles": search_by_tag(tag)})

if __name__ == "__main__":
    print("Starting server ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
