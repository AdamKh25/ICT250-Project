# server/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys

# Make sure we can import from project root (ciphers/, hacking/, etc.)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ciphers import caesar, vigenere, affine, transposition

app = Flask(__name__)
CORS(app)

# ---------- Health ----------
@app.get("/api/health")
def api_health():
    return jsonify({"ok": True})

# ---------- Encrypt ----------
@app.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    params = data.get("params") or {}

    try:
        if cipher == "caesar":
            key = int(params.get("key", 0))
            ct  = caesar.encrypt(text, key)
        elif cipher == "vigenere":
            key = str(params.get("key", ""))
            ct  = vigenere.encrypt(text, key)
        elif cipher == "affine":
            # key is the packed a*26 + b like in your class code
            key = int(params.get("key"))
            ct  = affine.encrypt(text, key)
        elif cipher == "transposition":
            key = int(params.get("key", 8))
            ct  = transposition.encrypt(text, key)
        else:
            return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

        return jsonify({"ok": True, "ciphertext": ct})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ---------- Decrypt ----------
@app.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    params = data.get("params") or {}

    try:
        if cipher == "caesar":
            key = int(params.get("key", 0))
            pt  = caesar.decrypt(text, key)
        elif cipher == "vigenere":
            key = str(params.get("key", ""))
            pt  = vigenere.decrypt(text, key)
        elif cipher == "affine":
            key = int(params.get("key"))
            pt  = affine.decrypt(text, key)
        elif cipher == "transposition":
            key = int(params.get("key", 8))
            pt  = transposition.decrypt(text, key)
        else:
            return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

        return jsonify({"ok": True, "plaintext": pt})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# --- Hack endpoints ---
@app.post("/api/hack/caesar")
def api_hack_caesar():
    data = request.get_json(force=True)
    ct = data.get("ciphertext", "")
    from ciphers import caesar

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
    from ciphers import affine
    import math

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
