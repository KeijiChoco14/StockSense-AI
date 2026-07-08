# 24. Changelog (Catatan Perubahan Sistem)

Seluruh pelacakan versi rilis perangkat lunak platform StockSense AI tunduk secara ketat pada aturan penomoran versi Semantic Versioning 2.0.0 (SemVer) dengan format tiga angka terpisah titik: MAJOR.MINOR.PATCH.

---

## [1.0.0-rc1] — 2026-07-08

### 🚀 Ditambahkan (Added)
- Inisialisasi dokumen fondasi arsitektur sistem utama StockSense AI secara lengkap di direktori /docs.
- Kerangka spesifikasi skema database PostgreSQL murni yang dilengkapi dengan protokol Row-Level Security (RLS) untuk keamanan multi-tenant.
- Desain kontrak RESTful API menggunakan FastAPI yang dilengkapi dengan pembungkus format respons seragam (Standard Response Wrapper).
- Arsitektur model AI deret waktu menggunakan jaringan saraf berulang (GRU Deep Learning) untuk modul prediksi ketersediaan bahan baku di masa depan.
- Token visual Design System yang diintegrasikan dengan Tailwind CSS dan aturan validasi skema form menggunakan pustaka Zod di sisi klien.

### 📝 Diubah (Changed)
- Siklus dokumentasi peta perjalanan pengguna (User Journey Map) disempurnakan menjadi diagram alur logis tanpa pembungkus ganda guna memastikan kemudahan proses penyalinan tanpa hambatan sintaks.