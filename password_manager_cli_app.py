import os
import json
import secrets
import string
from crypto_utils import CryptoUtils

class PasswordManager:
    def __init__(self, data_file="vault_data.json"):
        """Inisialisasi manajer kata sandi dan memuat data vault."""
        self.data_file = data_file
        self.crypto = CryptoUtils()
        self.vault = self.load_vault()
        self.master_key = None

    def load_vault(self):
        """Memuat berkas database kata sandi."""
        default_vault = {
            "master_hash": None,
            "master_salt": None,
            "credentials": []
        }
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return default_vault
        return default_vault

    def save_vault(self):
        """Menyimpan database kata sandi ke berkas JSON."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.vault, f, indent=4)

    def clear_screen(self):
        """Membersihkan layar terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        """Menampilkan header aplikasi yang bersih."""
        self.clear_screen()
        print("=" * 55)
        print("             SECURE PASSWORD VAULT CLI              ")
        print("=" * 55)

    def initialize_vault(self):
        """Membuat master password baru jika vault baru digunakan."""
        self.show_header()
        print("[ SETUP AWAL: BUAT MASTER PASSWORD ]\n")
        print("Master Password digunakan untuk mengenkripsi semua data Anda.")
        print("PENTING: Jangan sampai lupa! Jika lupa, data tidak bisa didekripsi.\n")
        
        while True:
            password = input("Masukkan Master Password Baru: ").strip()
            if len(password) < 6:
                print("❌ Master Password harus minimal 6 karakter!")
                continue
            
            confirm = input("Konfirmasi Master Password Baru: ").strip()
            if password != confirm:
                print("❌ Password tidak cocok! Silakan coba lagi.\n")
                continue
            
            # Buat hash dan salt baru
            salt = self.crypto.generate_salt()
            pwd_hash = self.crypto.hash_password(password, salt)
            
            self.vault["master_hash"] = pwd_hash
            self.vault["master_salt"] = salt
            self.save_vault()
            
            print("\n✅ Master Password berhasil dibuat!")
            input("Tekan Enter untuk melanjutkan ke login...")
            break

    def authenticate(self):
        """Melakukan autentikasi pengguna menggunakan Master Password."""
        self.show_header()
        print("[ MASUK KE VAULT ANDA ]\n")
        
        attempts = 3
        while attempts > 0:
            password = input("Masukkan Master Password: ").strip()
            salt = self.vault["master_salt"]
            saved_hash = self.vault["master_hash"]
            
            current_hash = self.crypto.hash_password(password, salt)
            
            if current_hash == saved_hash:
                # Turunkan kunci enkripsi simetris AES dari password + salt
                self.master_key = self.crypto.derive_key(password, salt)
                print("\n✅ Akses Diterima! Membuka brankas...")
                return True
            else:
                attempts -= 1
                print(f"❌ Password Salah! Sisa percobaan: {attempts}")
                
        print("\n❌ Terlalu banyak percobaan gagal. Program dihentikan.")
        return False

    def generate_random_password(self, length=16):
        """Menghasilkan kata sandi acak yang sangat kuat secara kriptografis."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        return "".join(secrets.choice(chars) for _ in range(length))

    def add_credential(self):
        """Menambahkan kredensial baru dengan enkripsi AES-256."""
        self.show_header()
        print("[ TAMBAH KREDENSIAL BARU ]\n")
        
        service = input("Nama Layanan (contoh: Google, Github): ").strip().capitalize()
        if not service:
            print("❌ Nama layanan tidak boleh kosong!")
            input("\nTekan Enter...")
            return

        username = input("Username / Email: ").strip()
        
        print("\nOpsi Kata Sandi:")
        print("1. Ketik kata sandi manual")
        print("2. Buat otomatis secara acak (Sangat Kuat)")
        opsi = input("Pilih (1/2): ").strip()
        
        if opsi == '2':
            password = self.generate_random_password()
            print(f"👉 Password yang dihasilkan: {password}")
        else:
            password = input("Masukkan Kata Sandi: ").strip()

        if not username or not password:
            print("❌ Username dan Password tidak boleh kosong!")
            input("\nTekan Enter...")
            return

        # Enkripsi password menggunakan master_key
        encrypted_password = self.crypto.encrypt(password, self.master_key)
        
        # Simpan kredensial baru
        self.vault["credentials"].append({
            "service": service,
            "username": username,
            "password": encrypted_password
        })
        self.save_vault()
        
        print(f"\n✅ Kredensial untuk '{service}' berhasil dienkripsi dan disimpan!")
        input("\nTekan Enter untuk kembali...")

    def list_credentials(self):
        """Menampilkan daftar kredensial yang tersimpan dan mendekripsinya."""
        self.show_header()
        print("[ DAFTAR KREDENSIAL ANDA ]\n")
        
        credentials = self.vault.get("credentials", [])
        if not credentials:
            print("Brankas Anda masih kosong. Silakan tambah kredensial baru.")
            input("\nTekan Enter...")
            return

        for idx, cred in enumerate(credentials, 1):
            print(f"{idx}. Layanan : {cred['service']}")
            print(f"   Username: {cred['username']}")
            # Dekripsi password secara real-time saat ditampilkan
            try:
                decrypted_password = self.crypto.decrypt(cred['password'], self.master_key)
                print(f"   Password: {decrypted_password}")
            except Exception:
                print("   Password: ❌ Gagal mendekripsi data!")
            print("-" * 45)

        input("\nTekan Enter untuk kembali...")

    def search_credential(self):
        """Mencari layanan tertentu di dalam vault."""
        self.show_header()
        print("[ CARI KREDENSIAL ]\n")
        
        query = input("Masukkan nama layanan yang dicari: ").strip().lower()
        if not query:
            return

        credentials = self.vault.get("credentials", [])
        found = False

        print("\nHasil Pencarian:")
        print("=" * 45)
        for cred in credentials:
            if query in cred['service'].lower():
                found = True
                print(f"📌 Layanan : {cred['service']}")
                print(f"   Username: {cred['username']}")
                try:
                    decrypted_password = self.crypto.decrypt(cred['password'], self.master_key)
                    print(f"   Password: {decrypted_password}")
                except Exception:
                    print("   Password: ❌ Gagal mendekripsi!")
                print("-" * 45)

        if not found:
            print("❌ Tidak ada kredensial yang cocok ditemukan.")
            
        input("\nTekan Enter untuk kembali...")

    def run(self):
        """Alur program utama."""
        # Jika belum ada master password, lakukan inisialisasi awal
        if not self.vault["master_hash"] or not self.vault["master_salt"]:
            self.initialize_vault()
            
        # Lakukan autentikasi masuk ke brankas
        if not self.authenticate():
            return

        # Menu utama brankas aman
        while True:
            self.show_header()
            print("1. Tambah Kredensial Akun")
            print("2. Lihat Semua Kredensial (Dekripsi Otomatis)")
            print("3. Cari Kredensial Layanan")
            print("4. Keluar dari Brankas")
            print("=" * 55)
            
            pilihan = input("Pilih opsi (1-4): ").strip()
            
            if pilihan == '1':
                self.add_credential()
            elif pilihan == '2':
                self.list_credentials()
            elif pilihan == '3':
                self.search_credential()
            elif pilihan == '4':
                self.show_header()
                # Hapus kunci dari memori sebelum keluar demi keamanan tambahan
                self.master_key = None
                print("\n🔐 Brankas berhasil dikunci kembali. Tetap aman!\n")
                break
            else:
                print("\n❌ Opsi tidak valid!")
                input("\nTekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()