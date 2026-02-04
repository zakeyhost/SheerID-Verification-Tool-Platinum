# SheerID Verification Tool Platinum Edition

Repositori ini berisi alat verifikasi SheerID tingkat lanjut yang dirancang untuk efisiensi dan keamanan data optimal. Sistem ini menggunakan arsitektur modern untuk memastikan proses verifikasi berjalan lancar dan sulit terdeteksi oleh sistem keamanan standar.

---

## Fitur Utama Platinum

**Advanced Anti Detection**
Penggunaan library `curl_cffi` memungkinkan impersonasi TLS yang akurat sehingga trafik terlihat seperti berasal dari browser Chrome asli. Fitur ini secara signifikan meningkatkan tingkat keberhasilan verifikasi dibandingkan dengan metode standar.

**Behavioral Simulation**
Sistem mengimplementasikan simulasi perilaku manusia saat mengisi formulir. Proses ini mencakup variasi kecepatan input dan jeda waktu yang dinamis untuk menghindari pemicu deteksi bot otomatis.

**Efficient SSO Bypass**
Integrasi khusus pada endpoint `DELETE /step/sso` memungkinkan bypass proses Single Sign-On yang tidak diperlukan. Hal ini mempercepat alur kerja verifikasi secara keseluruhan.

**Dynamic Document Generation**
Modul `doc_generator.py` mampu menghasilkan dokumen verifikasi dengan teknik noise injection. Setiap dokumen memiliki karakteristik unik untuk mencegah deteksi duplikasi oleh sistem pemindaian pihak ketiga.

**University Database Support**
Dukungan penuh telah dioptimasi untuk Arizona State University serta daftar institusi pendidikan global lainnya yang memiliki tingkat kepercayaan tinggi.

---

## Panduan Instalasi dan Penggunaan

**Persyaratan Sistem**
Pastikan Python telah terinstall di lingkungan kerja Anda kemudian jalankan perintah berikut untuk memasang dependensi yang diperlukan
```bash
pip install httpx Pillow curl_cffi python-dotenv
```

**Menjalankan Program**
Eksekusi script utama melalui terminal dengan perintah
```bash
python3 main_v2.py
```

---

## Spesifikasi Teknis

Sistem ini dikembangkan berdasarkan riset mendalam terhadap protokol keamanan SheerID terbaru. Seluruh metadata seperti ClientVersion dan NewRelic ID selalu diperbarui secara berkala menyesuaikan standar industri tahun 2026.

Fokus utama dari edisi Platinum ini adalah memberikan solusi verifikasi yang stabil, aman, dan memprioritaskan privasi pengguna melalui logika stealth yang ketat.

---
*Dikembangkan untuk profesional yang mengutamakan reliabilitas dan kecepatan.*
