# server/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, math

# project imports
from store.codec import save_note, load_note, list_titles, search_by_tag, b64e, b64d
from ciphers import caesar, vigenere, affine, transposition

app = Flask(__name__)
CORS(app)

# ---------- Health ----------
@app.get("/api/health")
def api_health():
    return jsonify({"ok": True, "service": "secure-notes-vault"})

# ---------- Encrypt/Decrypt ----------
@app.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(force=True)
    cipher = data.get("cipher", "").lower()
    text   = data.get("text", "")
    params = data.get("params", {}) or {}

    if cipher == "caesar":
        key = int(params.get("key", 0))
        ct  = caesar.encrypt(text, key)
    elif cipher == "vigenere":
        key = str(params.get("key", ""))
        ct  = vigenere.encrypt(text, key)
    elif cipher == "affine":
        a   = int(params.get("a", 5))
        b   = int(params.get("b", 8))
        key = a*26 + b
        ct  = affine.encrypt(text, key)
    elif cipher == "transposition":
        key = int(params.get("key", 8))
        ct  = transposition.encrypt(text, key)
    else:
        return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

    return jsonify({"ok": True, "ciphertext": ct})

@app.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(force=True)
    cipher = data.get("cipher", "").lower()
    text   = data.get("text", "")
    params = data.get("params", {}) or {}

    if cipher == "caesar":
        key = int(params.get("key", 0))
        pt  = caesar.decrypt(text, key)
    elif cipher == "vigenere":
        key = str(params.get("key", ""))
        pt  = vigenere.decrypt(text, key)
    elif cipher == "affine":
        a   = int(params.get("a", 5))
        b   = int(params.get("b", 8))
        key = a*26 + b
        pt  = affine.decrypt(text, key)
    elif cipher == "transposition":
        key = int(params.get("key", 8))
        pt  = transposition.decrypt(text, key)
    else:
        return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

    return jsonify({"ok": True, "plaintext": pt})

# ---------- Hack (Bruteforce) ----------
@app.post("/api/hack/caesar")
def api_hack_caesar():
    data = request.get_json(force=True)
    ct = data.get("ciphertext", "")
    candidates = []
    for k in range(26):
        pt = caesar.decrypt(ct, k)
        candidates.append({"key": k, "plaintext": pt})

    COMMON = (" THE ", " AND ", " TO ", " OF ", " IN ", " HELLO ", " WORLD ")
    def score(s):
        u = s.upper()
        return u.count(" ") + sum(u.count(w) for w in COMMON)

    best = max(candidates, key=lambda x: score(x["plaintext"]))
    return jsonify({"ok": True, "best": best, "candidates": candidates})

@app.post("/api/hack/affine")
def api_hack_affine():
    data = request.get_json(force=True)
    ct = data.get("ciphertext", "")
    M = 26
    validA = [a for a in range(1, M, 2) if math.gcd(a, M) == 1]
    candidates = []
    for a in validA:
        for b in range(M):
            key = a*26 + b
            try:
                pt = affine.decrypt(ct, key)
                candidates.append({"a": a, "b": b, "plaintext": pt})
            except Exception:
                pass

    COMMON = (" THE ", " AND ", " TO ", " OF ", " IN ", " HELLO ", " WORLD ", " NAME ")
    def score(s):
        u = s.upper()
        return u.count(" ") + sum(u.count(w) for w in COMMON)

    best = max(candidates, key=lambda x: score(x["plaintext"])) if candidates else None
    return jsonify({"ok": True, "best": best, "candidates": candidates})

# ---------- Notes (Save/List/Open/Search) ----------
@app.post("/api/note/save")
def api_note_save():
    data = request.get_json(force=True)
    title   = data["title"]
    tags    = data.get("tags", [])
    cipher  = data["cipher"]
    params  = data.get("params", {})
    plaintext = data["plaintext"]

    # encrypt with chosen cipher
    if cipher == "caesar":
        ct = caesar.encrypt(plaintext, int(params.get("key", 0)))
    elif cipher == "vigenere":
        ct = vigenere.encrypt(plaintext, str(params.get("key", "")))
    elif cipher == "affine":
        a = int(params.get("a", 5)); b = int(params.get("b", 8))
        ct = affine.encrypt(plaintext, a*26 + b)
    elif cipher == "transposition":
        ct = transposition.encrypt(plaintext, int(params.get("key", 8)))
    else:
        return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

    note = {
        "title": title,
        "tags": tags,
        "cipher": cipher,
        "params": params,
        "ciphertext_b64": b64e(ct),
    }
    os.makedirs("data/notes", exist_ok=True)
    save_note(os.path.join("data/notes", f"{title}.enc"), note)
    return jsonify({"ok": True})

@app.get("/api/note/list")
def api_note_list():
    os.makedirs("data/notes", exist_ok=True)
    return jsonify({"ok": True, "titles": list_titles("data/notes")})

@app.get("/api/note/open")
def api_note_open():
    title = request.args.get("title", "")
    path  = os.path.join("data/notes", f"{title}.enc")
    note  = load_note(path)
    return jsonify({"ok": True, "note": note})

@app.get("/api/note/search")
def api_note_search():
    tag = request.args.get("tag", "")
    hits = search_by_tag("data/notes", tag)
    return jsonify({"ok": True, "hits": hits})

if __name__ == "__main__":
    # Make sure all routes are defined BEFORE this line
    app.run(host="127.0.0.1", port=5000, debug=True)
