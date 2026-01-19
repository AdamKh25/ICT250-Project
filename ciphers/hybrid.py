from .otp import encrypt as otp_enc, decrypt as otp_dec, text_to_bytes
from .rsa import encrypt_int, PUBKEY, PRIVKEY, decrypt_int

def pack_with_rsa_otp(plaintext: str, pubkey=PUBKEY) -> tuple[bytes, bytes]:
    ct_str, otp_key = otp_enc(plaintext)
    ct_bytes = ct_str.encode()
    key_int = int.from_bytes(otp_key, 'big')
    rsa_ct = encrypt_int(key_int, pubkey)
    key_bytes = rsa_ct.to_bytes((rsa_ct.bit_length() + 7) // 8, 'big')
    return ct_bytes, key_bytes

def open_with_rsa_otp(payload_bytes: bytes, key_bytes: bytes, privkey=PRIVKEY) -> str:
    rsa_pt_int = int.from_bytes(key_bytes, 'big')
    otp_key_int = decrypt_int(rsa_pt_int, privkey)
    otp_key = otp_key_int.to_bytes((otp_key_int.bit_length() + 7) // 8, 'big')
    ct_str = payload_bytes.decode(errors='ignore')
    return otp_dec(ct_str, otp_key)

if __name__ == "__main__":
    orig = "Hybrid secure note!"
    payload, keyblob = pack_with_rsa_otp(orig)
    pt = open_with_rsa_otp(payload, keyblob)
    print(f"Hybrid: '{pt}' == '{orig}' → {pt == orig}")
