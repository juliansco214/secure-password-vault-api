from cryptography.fernet import Fernet
import os

def get_fernet():
    key = os.getenv("VAULT_KEY")
    if not key:
        raise RuntimeError("VAULT_KEY not set")
    return Fernet(key.encode())

def encrypt_password(plaintext: str) -> str:
    f = get_fernet()
    return f.encrypt(plaintext.encode()).decode()

def decrypt_password(ciphertext: str) -> str:
    f = get_fernet()
    return f.decrypt(ciphertext.encode()).decode()

