from validation import require_int

P, Q = 61, 53
N = P * Q
PHI = (P-1)*(Q-1)
E = 17
D = pow(E, -1, PHI)

PUBKEY = (E, N)
PRIVKEY = (D, N)

def encrypt_int(m: int, pubkey: tuple[int, int]) -> int:
    e, n = pubkey
    require_int('m', m, 0)
    if m >= n: raise ValueError("m < n required")
    return pow(m, e, n)

def decrypt_int(c: int, privkey: tuple[int, int]) -> int:
    d, n = privkey
    return pow(c, d, n)

if __name__ == "__main__":
    m = 42
    c = encrypt_int(m, PUBKEY)
    pt = decrypt_int(c, PRIVKEY)
    print(f"RSA: {m} → {c} → {pt}")

