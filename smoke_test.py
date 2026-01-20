import importlib, sys

def t(name, fn):
    try:
        fn()
        print(f"[OK] {name}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        raise

def test_caesar():
    m = importlib.import_module("ciphers.caesar")
    pt = "Hello, World!"
    c  = m.encrypt(pt, 3)
    d  = m.decrypt(c, 3)
    assert d == pt

def test_vigenere():
    m = importlib.import_module("ciphers.vigenere")
    pt, k = "Attack at dawn", "LEMON"
    c  = m.encrypt(pt, k)
    d  = m.decrypt(c, k)
    assert d == pt

def test_affine():
    m = importlib.import_module("ciphers.affine")
    key = 5*26 + 8   # a=5, b=8
    pt  = "HELLO world"
    c   = m.encrypt(pt, key)
    d   = m.decrypt(c, key)
    assert d == pt

def test_transposition():
    m = importlib.import_module("ciphers.transposition")
    pt = "WE ARE READY"
    c  = m.encrypt(pt, 4)
    d  = m.decrypt(c, 4)
    assert d == pt

def test_hack_caesar():
    m = importlib.import_module("hacking.caesar_hack")
    pt, key, _ = m.hack("KHOOR ZRUOG")
    assert "HELLO WORLD" in pt.upper() and key in range(26)

def test_hack_affine():
    m_aff = importlib.import_module("ciphers.affine")
    m     = importlib.import_module("hacking.affine_hack")
    key   = 5*26 + 8
    ct    = m_aff.encrypt("HELLO WORLD", key)
    pt, (a,b), _ = m.hack(ct)
    assert "HELLO WORLD" in pt.upper()
    assert a in (1,3,5,7,9,11,15,17,19,21,23,25)

def test_main_imports():
    import main, validation

if __name__ == "__main__":
    tests = [
        ("caesar", test_caesar),
        ("vigenere", test_vigenere),
        ("affine", test_affine),
        ("transposition", test_transposition),
        ("hack_caesar", test_hack_caesar),
        ("hack_affine", test_hack_affine),
        ("main_imports", test_main_imports),
    ]
    failures = 0
    for name, fn in tests:
        try:
            t(name, fn)
        except Exception:
            failures += 1
    if failures:
        sys.exit(1)
    print("\nAll smoke tests passed ✅")
