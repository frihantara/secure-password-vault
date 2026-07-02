# **🔑 Secure Password Vault (CLI System)**

**Secure Password Vault** adalah aplikasi pengelola kata sandi berbasis Command Line Interface (CLI) yang aman dan tangguh. Aplikasi ini dirancang untuk menyimpan kredensial akun Anda secara lokal dengan enkripsi standar industri **AES-256** (Fernet) dan sistem autentikasi Master Password menggunakan kombinasi algoritma hashing **SHA-256** ditambah dengan penggaraman (*salting*).

Proyek ini mendemonstrasikan implementasi keamanan siber praktis, manajemen ketergantungan Python, pemisahan tugas secara modular, serta pengujian unit (*Unit Testing*).

## **✨ Fitur Unggulan**

* **🔐 Autentikasi Master Password**: Akses ke dalam brankas dilindungi oleh satu Master Password yang di-hash dengan aman menggunakan garam (*salt*) unik dan algoritma SHA-256.  
* **🛡️ Enkripsi AES-256 Militer**: Semua kata sandi akun yang Anda simpan dienkripsi menggunakan pustaka cryptography sebelum ditulis ke penyimpanan lokal (vault\_data.json). Data tidak dapat didekripsi atau dibaca tanpa kunci master yang tepat.  
* **🎲 Generator Kata Sandi Kuat**: Dilengkapi dengan pembuat kata sandi acak otomatis yang aman (kombinasi huruf besar, huruf kecil, angka, dan simbol khusus).  
* **🔍 Pencarian Cepat**: Cari kredensial berdasarkan nama layanan (misal: Google, GitHub) dengan mudah dan cepat.  
* **🧹 Keamanan Memori**: Menghapus kunci enkripsi dari memori utama setelah Anda keluar dari aplikasi untuk mencegah kebocoran data.

## **📂 Struktur Repositori**

secure-password-vault/  
│  
├── password\_manager.py   \# Aplikasi Utama: Menu interaktif dan alur logika vault  
├── crypto\_utils.py       \# Modul Kriptografi: Enkripsi, dekripsi, dan hashing password  
├── test\_crypto.py        \# Modul Pengujian: Unit testing untuk keandalan fungsi enkripsi  
├── requirements.txt      \# Daftar dependensi eksternal (Pustaka Kriptografi)  
└── README.md             \# Dokumentasi lengkap petunjuk penggunaan

## **🚀 Panduan Memulai & Penggunaan**

### **1\. Persiapan Awal**

Pastikan Anda sudah menginstal Python (versi 3.8 ke atas) di perangkat Anda.

### **2\. Instalasi Dependensi**

Instal pustaka keamanan eksternal yang diperlukan menggunakan file requirements.txt dengan menjalankan perintah berikut di terminal Anda:

pip install \-r requirements.txt

### **3\. Jalankan Aplikasi Utama**

Saat pertama kali dijalankan, sistem akan mendeteksi bahwa brankas belum terbuat dan meminta Anda untuk membuat **Master Password** baru.

⚠️ **PENTING**: *Jangan sampai melupakan Master Password Anda\! Jika Anda lupa, data kata sandi yang tersimpan di dalam brankas tidak akan pernah bisa dipulihkan.*

python password\_manager.py

### **4\. Menjalankan Uji Otomatis (Unit Testing)**

Untuk memverifikasi bahwa modul enkripsi dan dekripsi berjalan dengan akurasi dan keamanan 100%:

python \-m unittest test\_crypto.py

## **🎨 Ilustrasi Alur Kerja Keamanan (Security Flow)**

\[Input Kata Sandi\] ──\> \[Enkripsi AES-256\] ──\> \[Disimpan di vault\_data.json (Teks Acak)\]  
                                                     │  
\[Teks Terenkripsi\] \<── \[Dekripsi AES-256\] \<── \[Akses Berhasil dengan Master Password\]

## **🤝 Kontribusi**

Saran pengembangan sangat terbuka\! Jika Anda ingin meningkatkan fungsionalitas aplikasi ini (seperti menambahkan fitur ekspor data terenkripsi atau integrasi keamanan lainnya), silakan lakukan fork pada repositori ini dan kirimkan Pull Request terbaik Anda.

*Keamanan data Anda adalah prioritas utama. Gunakan pengelola kata sandi lokal ini untuk mengamankan identitas digital Anda secara mandiri.*