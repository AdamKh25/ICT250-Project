from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys

# Make sure Python can see ciphers/ and hacking/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ciphers import caesar, vigenere, affine, transposition
from hacking import caesar_hack, affine_hack

app = Flask(__name__)
CORS(app)

# ---------- Health ----------
@app.get("/api/health")
def api_health():
    return jsonify({"ok": True, "service": "crypto_toolkit"})

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
            a = params.get("a")
            b = params.get("b")

            if a is None or b is None:
                raise ValueError("Affine cipher requires parameters 'a' and 'b'")

            a = int(a)
            b = int(b)

            key = a * 26 + (b % 26)
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
            a = params.get("a")
            b = params.get("b")

            if a is None or b is None:
                raise ValueError("Affine cipher requires parameters 'a' and 'b'")

            a = int(a)
            b = int(b)

            key = a * 26 + (b % 26)
            pt  = affine.decrypt(text, key)

        elif cipher == "transposition":
            key = int(params.get("key", 8))
            pt  = transposition.decrypt(text, key)

        else:
            return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

        return jsonify({"ok": True, "plaintext": pt})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


# ---------- Hack: Caesar ----------
@app.post("/api/hack/caesar")
def api_hack_caesar():
    data = request.get_json(force=True, silent=True) or {}
    ct = data.get("ciphertext") or data.get("text") or ""

    pt, key, candidates = caesar_hack.hack(ct)

    return jsonify({
        "ok": True,
        "plaintext": pt,
        "key": key,
        "candidates": candidates[:10],
    })


# ---------- Hack: Affine ----------
@app.post("/api/hack/affine")
def api_hack_affine():
    data = request.get_json(force=True, silent=True) or {}
    ct = data.get("ciphertext") or data.get("text") or ""

    pt, (a, b), candidates = affine_hack.hack(ct)

    return jsonify({
        "ok": True,
        "plaintext": pt,
        "a": a,
        "b": b,
        "candidates": candidates[:10],
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
