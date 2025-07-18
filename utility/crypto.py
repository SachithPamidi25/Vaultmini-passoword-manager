from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, base64

def encrypt_password(plain_text:str, key:bytes)->str:
    aesgcm=AESGCM(key)
    nonce=os.urandom(12)
    ct=aesgcm.encrypt(nonce, plain_text.encode(), None)
    return base64.b64encode(nonce+ct).decode()

def decrypt_password(enc_text:str, key:bytes)->str:
    aesgcm=AESGCM(key)
    raw=base64.b64decode(enc_text.encode())
    nonce=raw[:12]
    ct=raw[12:]
    return aesgcm.decrypt(nonce, ct, None).decode()

def generate_key()->bytes:
    return AESGCM.generate_key(bit_length=128)