import unittest
from crypto_utils import CryptoUtils

class TestCryptoUtils(unittest.TestCase):
    def setUp(self):
        """Inisialisasi modul kriptografi sebelum pengujian."""
        self.crypto = CryptoUtils()
        self.dummy_password = "SuperSecretMaster123!"
        self.dummy_salt = self.crypto.generate_salt()

    def test_salt_uniqueness(self):
        """Memastikan garam (salt) yang dihasilkan selalu unik setiap waktu."""
        salt1 = self.crypto.generate_salt()
        salt2 = self.crypto.generate_salt()
        self.assertNotEqual(salt1, salt2)

    def test_password_hashing(self):
        """Menguji apakah fungsi hashing SHA-256 konsisten dan aman."""
        hash1 = self.crypto.hash_password(self.dummy_password, self.dummy_salt)
        hash2 = self.crypto.hash_password(self.dummy_password, self.dummy_salt)
        
        # Hash harus sama untuk password dan salt yang sama
        self.assertEqual(hash1, hash2)
        
        # Hash harus berbeda jika salt berbeda
        different_salt = self.crypto.generate_salt()
        hash3 = self.crypto.hash_password(self.dummy_password, different_salt)
        self.assertNotEqual(hash1, hash3)

    def test_encryption_decryption(self):
        """Menguji alur enkripsi AES-256 dan kemampuan pemulihan data asli."""
        secret_data = "PasswordRahasiaBank123"
        
        # Turunkan kunci simetris
        key = self.crypto.derive_key(self.dummy_password, self.dummy_salt)
        
        # Lakukan enkripsi
        encrypted = self.crypto.encrypt(secret_data, key)
        self.assertNotEqual(secret_data, encrypted)  # Teks enkripsi tidak boleh sama dengan teks asli

        # Lakukan dekripsi
        decrypted = self.crypto.decrypt(encrypted, key)
        self.assertEqual(secret_data, decrypted)  # Hasil dekripsi harus cocok sempurna dengan aslinya

if __name__ == "__main__":
    unittest.main()