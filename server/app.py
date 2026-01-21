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
