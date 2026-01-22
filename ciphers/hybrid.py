from ciphers import otp, rsa


# encrypt message using otp and protect key with rsa
def pack_with_rsa_otp(plaintext, pub):
    # encrypt plaintext with otp and generate random key
    ct, key = otp.encrypt(plaintext, None)

    # encrypt otp key using rsa public key
    key_blocks = rsa.encrypt(key, pub)

    # return encrypted message and encrypted key
    return {"ciphertext": ct, "key_blocks": key_blocks}


# decrypt message by recovering otp key with rsa
def open_with_rsa_otp(payload, priv):
    # decrypt otp key using rsa private key
    key = rsa.decrypt(payload["key_blocks"], priv)

    # decrypt ciphertext using recovered otp key
    pt = otp.decrypt(payload["ciphertext"], key)

    return pt
