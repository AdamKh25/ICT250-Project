from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys

# ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# import cipher and hacking modules
from ciphers import caesar, vigenere, affine, transposition
from hacking import caesar_hack, affine_hack

# create flask app
app = Flask(__name__)

# enable cors for frontend access
CORS(app)


# ---------- health ----------
@app.get("/api/health")
def api_health():
    # simple backend status check
    return jsonify({"ok": True, "service": "crypto_toolkit"})


# ---------- encrypt ----------
@app.post("/api/encrypt")
def api_encrypt():
    # parse request json
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    params = data.get("params") or {}

    try:
        # caesar encryption
        if cipher == "caesar":
            key = int(params.get("key", 0))
            ct  = caesar.encrypt(text, key)

        # vigenere encryption
        elif cipher == "vigenere":
            key = str(params.get("key", ""))
            ct  = vigenere.encrypt(text, key)

        # affine encryption
        elif cipher == "affine":
            a = params.get("a")
            b = params.get("b")

            # require both a and b
            if a is None or b is None:
                raise ValueError("Affine cipher requires parameters 'a' and 'b'")

            a = int(a)
            b = int(b)

            # pack a and b into single key
            key = a * 26 + (b % 26)
            ct  = affine.encrypt(text, key)

        # transposition encryption
        elif cipher == "transposition":
            key = int(params.get("key", 8))
            ct  = transposition.encrypt(text, key)

        # unsupported cipher
        else:
            return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

        # return ciphertext
        return jsonify({"ok": True, "ciphertext": ct})

    except Exception as e:
        # return error message
        return jsonify({"ok": False, "error": str(e)}), 400


# ---------- decrypt ----------
@app.post("/api/decrypt")
def api_decrypt():
    # parse request json
    data = request.get_json(force=True)
    cipher = (data.get("cipher") or "").lower()
    text   = data.get("text") or ""
    params = data.get("params") or {}

    try:
        # caesar decryption
        if cipher == "caesar":
            key = int(params.get("key", 0))
            pt  = caesar.decrypt(text, key)

        # vigenere decryption
        elif cipher == "vigenere":
            key = str(params.get("key", ""))
            pt  = vigenere.decrypt(text, key)

        # affine decryption
        elif cipher == "affine":
            a = params.get("a")
            b = params.get("b")

            # require both a and b
            if a is None or b is None:
                raise ValueError("Affine cipher requires parameters 'a' and 'b'")

            a = int(a)
            b = int(b)

            # pack a and b into single key
            key = a * 26 + (b % 26)
            pt  = affine.decrypt(text, key)

        # transposition decryption
        elif cipher == "transposition":
            key = int(params.get("key", 8))
            pt  = transposition.decrypt(text, key)

        # unsupported cipher
        else:
            return jsonify({"ok": False, "error": f"Unknown cipher '{cipher}'"}), 400

        # return plaintext
        return jsonify({"ok": True, "plaintext": pt})

    except Exception as e:
        # return error message
        return jsonify({"ok": False, "error": str(e)}), 400


# ---------- hack: caesar ----------
@app.post("/api/hack/caesar")
def api_hack_caesar():
    # parse request json safely
    data = request.get_json(force=True, silent=True) or {}
    ct = data.get("ciphertext") or data.get("text") or ""

    # run caesar brute force
    pt, key, candidates = caesar_hack.hack(ct)

    # return best guess and candidates
    return jsonify({
        "ok": True,
        "plaintext": pt,
        "key": key,
        "candidates": candidates[:10],
    })


# ---------- hack: affine ----------
@app.post("/api/hack/affine")
def api_hack_affine():
    # parse request json safely
    data = request.get_json(force=True, silent=True) or {}
    ct = data.get("ciphertext") or data.get("text") or ""

    # run affine brute force
    pt, (a, b), candidates = affine_hack.hack(ct)

    # return best guess and candidates
    return jsonify({
        "ok": True,
        "plaintext": pt,
        "a": a,
        "b": b,
        "candidates": candidates[:10],
    })


# start flask server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
