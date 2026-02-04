SheerID Verification Tool - Platinum Edition

Repositori ini berisi alat verifikasi SheerID yang dioptimalkan untuk layanan Gemini AI dan YouTube Premium. Versi Platinum ini fokus pada keamanan stealth dan kualitas dokumen yang dihasilkan agar lolos verifikasi otomatis maupun manual.

FITUR UTAMA

1. Advanced Anti-Detection
Menggunakan library curl_cffi untuk meniru fingerprint browser Chrome asli. Ini membuat trafik bot tidak terdeteksi sebagai script Python oleh firewall Cloudflare atau Akamai.

2. Realistic Document Generator
Modul doc_enhancer.py dirancang untuk membuat dokumen (Transkrip/KTM) yang terlihat seperti hasil scan atau foto kamera HP.
- Menambahkan noise (bintik) pada gambar.
- Rotasi kemiringan acak (glitch effect) agar tidak terlihat terlalu simetris.
- Injeksi siluet foto profil untuk menghindari deteksi AI pada kartu identitas.
- Format output JPEG dengan kompresi yang menyerupai kamera asli.

3. Telegram Bot Integration
Fitur bot Telegram pribadi untuk memudahkan eksekusi tanpa perlu membuka terminal setiap saat. Cukup kirim link verifikasi ke bot, dan proses akan berjalan di background.

4. Optimization
- Bypass SSO (Login Portal Kampus) secara otomatis.
- Menggunakan database universitas dengan tingkat keberhasilan tinggi.

INSTALASI

Pastikan Python 3.10 ke atas sudah terinstall.

1. Clone repositori dan masuk ke direktori folder.
2. Buat virtual environment (opsional tapi disarankan):
   python -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
   (atau manual: pip install httpx Pillow curl_cffi python-dotenv python-telegram-bot faker numpy requests)

KONFIGURASI

Buat file bernama .env di dalam folder utama, lalu isi dengan format berikut:

PROXY_URL=http://user:pass@ip:port
TELEGRAM_BOT_TOKEN=token_bot_anda_disini

PENGGUNAAN

Ada dua cara untuk menggunakan alat ini:

Cara 1: Mode Terminal (Manual)
Jalankan perintah ini di terminal untuk memproses satu link:
python main_v2.py "LINK_VERIFIKASI_SHEERID"

Cara 2: Mode Bot Telegram (Otomatis)
Jalankan bot di server/local:
python telegram_bot.py

Setelah bot berjalan, buka Telegram dan kirim perintah:
/verify LINK_VERIFIKASI_SHEERID

ALAT TAMBAHAN

verify_readiness.py
Script untuk mengecek apakah semua library dan fungsi generator dokumen berjalan normal sebelum melakukan eksekusi asli. Sangat disarankan dijalankan pertama kali.

DISCLAIMER

Alat ini dibuat untuk tujuan riset keamanan dan edukasi. Segala risiko penggunaan menjadi tanggung jawab pengguna.
