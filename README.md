![Platinum Banner](platinum_banner.png)

# SHEERID VERIFICATION TOOL
### PLATINUM EDITION — RELEASE 2.0

> **Sistem verifikasi otomatis tingkat lanjut dengan bypass anti-fraud dan generator dokumen ultra-realistis.**

---
### TECH STACK
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-image_processing-blue?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

---

## CORE CAPABILITIES

### STEALTH AND ANTI DETECT
Sistem ini tidak menggunakan Selenium atau browser automation yang mudah terdeteksi.

*   **TLS Spoofing** - Menggunakan `curl_cffi` untuk meniru fingerprint kriptografi Chrome 131 secara identik.
*   **Header Rotation** - Rotasi User-Agent dan Header Order dinamis untuk menghindari tracking statis.
*   **IP Masking** - Integrasi proxy residential untuk menyamarkan lokasi asli.

### REALISTIC DOCUMENT FORGERY
Generator dokumen cerdas yang dirancang untuk mengelabui sistem verifikasi visual.

*   **JPEG Artifacts** - Output gambar memiliki kompresi natural layaknya foto kamera HP.
*   **Organic Imperfections** - Menambahkan efek rotasi, noise bintik film, dan pencahayaan tidak merata.
*   **Silhouette Injection** - Kartu identitas dilengkapi siluet manusia realistis.

### TELEGRAM BOT INTERFACE
Kontrol full sistem verifikasi dari aplikasi Telegram.

*   **One Click Verify** - Kirim link dan bot memproses di background.
*   **Real time Status** - Notifikasi langsung saat verifikasi sukses atau butuh tindakan manual.

---

## DEPLOYMENT GUIDE

### PREREQUISITES
Pastikan Python 3.10+ sudah terinstall.

```bash
# Clone Repository & Setup Environment
git clone https://github.com/privatesector/sheerid-platinum.git
python -m venv .venv
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### CONFIGURATION
Buat file `.env` untuk menyimpan akses kunci.

```ini
PROXY_URL=http://user:pass@residential-proxy.com:port
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjkLmnOPqrstUVwxyz
TELEGRAM_API_ID=12345
TELEGRAM_API_HASH=abcdef12345
```

---

## OPERATION MODES

| MODE | COMMAND | FUNGSI |
| :--- | :--- | :--- |
| **BOT AUTO** | `python telegram_bot.py` | Menjalankan server bot Telegram. |
| **CLI MANUAL** | `python main_v2.py "URL"` | Memproses satu link secara manual. |
| **DIAGNOSTIC** | `python verify_readiness.py` | Self check sistem sebelum eksekusi. |

---

## DISCLAIMERS
> *Tool ini dikembangkan semata-mata untuk keperluan riset keamanan dan pengujian sistem. Pengembang tidak bertanggung jawab atas penyalahgunaan fitur yang ada di dalamnya.*

**COPYRIGHT 2026 PLATINUM DEV TEAM**
