from ciphers import otp, rsa

def pack_with_rsa_otp(plaintext, pub):
    ct, key = otp.encrypt(plaintext, None)  # random OTP key for letters
    key_blocks = rsa.encrypt(key, pub)      # encrypt the OTP key with RSA
    return {"ciphertext": ct, "key_blocks": key_blocks}

def open_with_rsa_otp(payload, priv):
    key = rsa.decrypt(payload["key_blocks"], priv)
    pt = otp.decrypt(payload["ciphertext"], key)
    return pt
