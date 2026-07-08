# 10. System Architecture & High-Level Design

StockSense AI mengadopsi prinsip **Clean Architecture** yang dikombinasikan dengan struktur berbasis domain fitur (*Feature-based structure*). Pemisahan ini menjamin kode tetap modular, mudah diuji (*testable*), dan tidak bergantung erat pada framework tertentu.

---

## 1. Lapisan Arsitektur (Architectural Layers)

Sistem dibagi menjadi empat lapisan utama dengan aturan ketergantungan searah (lapisan dalam tidak boleh mengetahui lapisan luar):

1.  **Domain / Entities Layer (Lapisan Terdalam)**
    * Berisi model data murni dan aturan bisnis inti yang sangat jarang berubah.
    * Bebas dari framework, ORM (SQLAlchemy), atau library eksternal.
2.  **Use Cases / Service Layer**
    * Berisi logika bisnis spesifik aplikasi (misalnya: alur verifikasi draf PO, kalkulasi masa kedaluwarsa).
    * Mengatur aliran data ke dan dari entitas.
3.  **Interface Adapters / Repository & Controller Layer**
    * **Repository**: Mengonversi data dari database menjadi objek entitas domain.
    * **Routers / Controllers**: Menerima request HTTP, melakukan validasi skema input (Pydantic), dan mengembalikan response JSON.
4.  **Frameworks & Drivers (Lapisan Terluar)**
    * Tempat bertempatnya FastAPI, SQLAlchemy, mesin database PostgreSQL, dan sistem eksternal lainnya.

---

## 2. Struktur Direktori Proyek Backend (Feature-Based)

Untuk mencegah penumpukan file saat skala aplikasi membesar, struktur folder diatur berdasarkan fitur bisnis, bukan berdasarkan tipe file teknis:

backend/
├── app/
│   ├── config/             # Konfigurasi global & Environment Variables (.env)
│   ├── database/           # Manajemen sesi async engine & registrasi Base Model
│   ├── middleware/         # Auth, JWT Validation, & Tenant RLS Scope Context
│   └── features/           # Modul fitur bisnis terisolasi
│       ├── auth/           # Otentikasi & Registrasi User
│       ├── inventory/      # Manajemen Stok & Bahan Baku
│       │   ├── models.py       # Skema tabel SQLAlchemy
│       │   ├── schemas.py      # Validasi skema input/output Pydantic
│       │   ├── repository.py   # Operasi database murni (SQL)
│       │   ├── service.py      # Logika bisnis inventaris murni
│       │   └── router.py       # Endpoint API FastAPI
│       ├── forecast/       # Inferensi AI & Prediksi Stok Out
│       └── procurement/    # Alur Kerja Purchase Order (PO)
├── alembic/                # File migrasi database otomatis
├── tests/                  # Skrip pengujian otomatis (PyTest)
└── main.py                 # Titik masuk aplikasi (FastAPI Instance)

---

## 3. Desain Komunikasi Data (Data Flow Pattern)

Setiap request yang masuk ke API harus mengikuti jalur linier yang konsisten tanpa melompati lapisan:

[HTTP Request] 
      │
      ▼
[FastAPI Router] ──► Validasi tipe data payload menggunakan Pydantic Schemas
      │
      ▼
[Service Layer]  ──► Eksekusi aturan bisnis (kalkulasi, pengecekan logika)
      │
      ▼
[Repository]     ──► Komunikasi data async ke PostgreSQL menggunakan SQLAlchemy 2.0
      │
      ▼
[Database Log]   ──► Mengembalikan data ke atas hingga menjadi HTTP JSON Response

---

## 4. Strategi Skalabilitas Komputasi AI

Proses prediksi deep learning (GRU Model) membutuhkan komputasi CPU/GPU yang intensif. Untuk mencegah server API FastAPI mengalami pemblokiran (*blocking threads*), arsitektur memisahkan jalur inferensi:
* **API Thread**: Hanya melayani operasi baca/tulis cepat (CRUD) dan membaca hasil prediksi yang sudah matang dari database.
* **Background Worker**: Proses kalkulasi prediksi AI dijalankan secara asinkron di latar belakang menggunakan antrean tugas (*Task Queue*) terpisah, memastikan performa aplikasi web tetap responsif di bawah 200ms bagi pengguna akhir.