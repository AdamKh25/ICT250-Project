# server/app.py
import os, sys
# --- Ensure project root is on sys.path so "ciphers", "hacking", "validation" import ---
ROOT = os.path.dirname(os.path.dirname(__file__))  # .../secure_notes_vault
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from flask import Flask, request, jsonify
from flask_cors import CORS

# Verbose import helper: prints the real reason if an import fails
def _try(path):
    try:
        return __import__(path, fromlist=["*"])
    except Exception as e:
        print(f"[IMPORT FAIL] {path}: {e}")
        return None

# Try to import your modules (they can be None if missing/broken)
validation    = _try("validation")
caesar        = _try("ciphers.caesar")
vigenere      = _try("ciphers.vigenere")
affine        = _try("ciphers.affine")
transposition = _try("ciphers.transposition")
cz_hack       = _try("hacking.caesar_hack")
af_hack       = _try("hacking.affine_hack")

app = Flask(__name__)
CORS(app)

def ok(data, status=200): return jsonify({"ok": True, **data}), status
def err(msg, status=400): return jsonify({"ok": False, "error": msg}), status

@app.get("/api/health")
def health():
    return ok({"status": "up"})

@app.post("/api/encrypt")
def api_encrypt():
    body = request.get_json(silent=True) or {}
    cipher = (body.get("cipher") or "").lower()
    text   = body.get("text") or ""
    params = body.get("params") or {}
    try:
        if cipher == "caesar":
            if not caesar: return err("Caesar module not available", 501)
            key = int(params.get("key"))
            return ok({"ciphertext": caesar.encrypt(text, key)})

        elif cipher == "vigenere":
            if not vigenere: return err("Vigenere module not available", 501)
            key = str(params.get("key") or "")
            return ok({"ciphertext": vigenere.encrypt(text, key)})

        elif cipher == "affine":
            if not affine: return err("Affine module not available", 501)
            if not validation: return err("validation module not available", 501)
            a = int(params.get("a")); b = int(params.get("b"))
            if not getattr(validation, "is_valid_affine_a")(a):
                return err("Invalid a: gcd(a,26) must be 1")
            key = getattr(validation, "make_affine_key")(a, b)
            return ok({"ciphertext": affine.encrypt(text, key)})

        elif cipher == "transposition":
            if not transposition: return err("Transposition module not available", 501)
            key = int(params.get("key"))
            if key < 2: return err("Key must be >= 2")
            return ok({"ciphertext": transposition.encrypt(text, key)})

        else:
            return err("Unknown cipher")
    except Exception as e:
        return err(str(e), 400)

@app.post("/api/decrypt")
def api_decrypt():
    body = request.get_json(silent=True) or {}
    cipher = (body.get("cipher") or "").lower()
    text   = body.get("text") or ""
    params = body.get("params") or {}
    try:
        if cipher == "caesar":
            if not caesar: return err("Caesar module not available", 501)
            key = int(params.get("key"))
            return ok({"plaintext": caesar.decrypt(text, key)})

        elif cipher == "vigenere":
            if not vigenere: return err("Vigenere module not available", 501)
            key = str(params.get("key") or "")
            return ok({"plaintext": vigenere.decrypt(text, key)})

        elif cipher == "affine":
            if not affine: return err("Affine module not available", 501)
            if not validation: return err("validation module not available", 501)
            a = int(params.get("a")); b = int(params.get("b"))
            if not getattr(validation, "is_valid_affine_a")(a):
                return err("Invalid a: gcd(a,26) must be 1")
            key = getattr(validation, "make_affine_key")(a, b)
            return ok({"plaintext": affine.decrypt(text, key)})

        elif cipher == "transposition":
            if not transposition: return err("Transposition module not available", 501)
            key = int(params.get("key"))
            if key < 2: return err("Key must be >= 2")
            return ok({"plaintext": transposition.decrypt(text, key)})

        else:
            return err("Unknown cipher")
    except Exception as e:
        return err(str(e), 400)

@app.post("/api/hack")
def api_hack():
    body = request.get_json(silent=True) or {}
    name = (body.get("cipher") or "").lower()
    ct   = body.get("ciphertext") or ""
    try:
        if name == "caesar":
            if not cz_hack: return err("Caesar hack not available", 501)
            pt, key, top = cz_hack.hack(ct)
            return ok({"plaintext": pt, "key": key, "top": top})

        elif name == "affine":
            if not af_hack: return err("Affine hack not available", 501)
            pt, (a,b), top = af_hack.hack(ct)
            return ok({"plaintext": pt, "a": a, "b": b, "top": top})

        else:
            return err("Unknown/unsupported hack")
    except Exception as e:
        return err(str(e), 400)

if __name__ == "__main__":
    # Run from project root: C:\Users\KATANA\Projects\secure_notes_vault
    app.run(host="127.0.0.1", port=5000, debug=True)
