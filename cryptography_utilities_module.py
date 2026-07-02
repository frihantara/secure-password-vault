import base64
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class CryptoUtils:
    def __init__(self):
        pass

    def generate_salt(self):
        """Menghasilkan salt acak bertipe heksadesimal untuk mengamankan hashing."""
        return os.urandom(16).hex()

    def hash_password(self, password, salt):
        """Melakukan hashing password menggunakan kombinasi salt dan SHA-256."""
        combined = password + salt
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def derive_key(self, password, salt):
        """Menurunkan kunci kriptografi Fernet AES-256 menggunakan PBKDF2HMAC."""
        salt_bytes = bytes.fromhex(salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=100000,  # Jumlah iterasi tinggi untuk mencegah serangan brute-force
        )
        # Menghasilkan kunci 32-byte dan dikodekan ke dalam format URL safe base64
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key

    def encrypt(self, plain_text, key):
        """Mengenkripsi teks biasa menggunakan algoritma simetris Fernet (AES-256)."""
        f = Fernet(key)
        encrypted_bytes = f.encrypt(plain_text.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')

    def decrypt(self, cipher_text, key):
        """Mendekripsi teks acak terenkripsi kembali ke teks asli."""
        f = Fernet(key)
        decrypted_bytes = f.decrypt(cipher_text.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')