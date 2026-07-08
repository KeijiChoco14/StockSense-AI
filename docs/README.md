# StockSense AI - Documentation Hub

Selamat datang di repositori dokumentasi resmi **StockSense AI**, sebuah *AI-Powered Decision Intelligence Platform* yang dirancang khusus untuk industri restoran skala enterprise.

Dokumentasi ini berfungsi sebagai *Single Source of Truth* (SSOT) untuk seluruh tim cross-functional: Produk, Teknikal, Desain, AI/ML, DevOps, dan QA. Seluruh keputusan arsitektur, batasan fitur, dan panduan penulisan kode wajib merujuk pada dokumen yang ada di dalam direktori ini.

---

## 📁 Struktur & Navigasi Dokumentasi

Seluruh dokumen arsitektur dan spesifikasi diatur secara modular di dalam direktori `/docs`. Anda dapat membaca dokumen secara berurutan atau langsung melompat ke bagian yang spesifik sesuai kebutuhan peran Anda:

### 🌟 Fondasi Bisnis & Produk
* [01. Project Overview](01_project_overview.md) — Visi, Misi, Masalah Utama, dan Solusi Platform.
* [02. Product Requirement Document (PRD)](02_prd.md) — Cakupan MVP, Matriks Fitur Inti, dan Kriteria Rilis.
* [03. Business & Market Analysis](03_business_market_analysis.md) — TAM/SAM/SOM, Unit Economics, dan Pricing Tiers.
* [04. Competitor Analysis](04_competitor_analysis.md) — Lanskap Kompetisi, Keunggulan Teknis, dan Paritas Fitur.

### 👥 Desain Berpusat Pada Pengguna (User-Centric Design)
* [05. User Personas](05_user_personas.md) — Profil Mendalam Pengguna Multi-Peran (Owner, Manajer, Chef, Gudang).
* [06. User Journey](06_user_journey.md) — Peta Perjalanan Pengguna dalam Siklus Pengisian Stok Otomatis.
* [07. User Stories](07_user_stories.md) — Daftar Cerita Pengguna Berdasarkan Epics untuk Backlog Sprint.

### 📐 Spesifikasi Sistem & Data
* [08. Functional Requirements](08_functional_requirements.md) — Spesifikasi Kebutuhan Fungsional Sistem & Aturan Bisnis.
* [09. Non-Functional Requirements](09_non_functional_requirements.md) — Target Latency ($P_{95}$), Skalabilitas, Konkurensi, dan SLA.
* [10. System Architecture](10_system_architecture.md) — Implementasi Clean Architecture & Pola Desain Backend/Frontend.
* [11. Database Design](11_database_design.md) — Skema Tabel PostgreSQL, Konvensi UUID, dan Strategi Indeks.
* [12. Entity Relationship Diagram (ERD)](12_erd.md) — Relasi Data Mutlak, Cascade Rules, dan Kamus Data.
* [13. API Specification](13_api_specification.md) — Kontrak RESTful API FastAPI, Format Response Wrapper, & Versioning.

### 🧠 Kecerdasan Buatan & Pipeline ML
* [14. AI Architecture](14_ai_architecture.md) — Desain Decision Intelligence & Kerangka Kerja Explainable AI (XAI).
* [15. ML Pipeline](15_ml_pipeline.md) — Siklus Hidup Data, Model GRU TensorFlow, & Strategi Mengatasi Cold Start.

### 🎨 Antarmuka & Token Desain
* [16. UI Guidelines](16_ui_guidelines.md) — Filosofi Estetika Visual Premium (Linear/Stripe Style).
* [17. Design System](17_design_system.md) — Token Warna, Tipografi, Komponen shadcn/ui, dan Validasi Zod.

### 💻 Standar Rekayasa & Operasional
* [18. Coding Guidelines](18_coding_guidelines.md) — Standar Kode Clean Python (FastAPI Async) & Next.js 15.
* [19. Security](19_security.md) — Implementasi Row-Level Security (RLS) PostgreSQL & Protokol JWT.
* [20. Testing Strategy](20_testing_strategy.md) — Piramida Pengujian Otomatis (Unit, Integration, E2E, ML Testing).
* [21. Deployment](21_deployment.md) — Strategi CI/CD GitHub Actions, Dockerization, Railway, & Vercel.

### 🚀 Keberlanjutan Proyek
* [22. Roadmap](22_roadmap.md) — Milestone Pengembangan Produk Fase 1, 2, dan 3.
* [23. Contributing](23_contributing.md) — Panduan Git Workflow dan Aturan Pull Request Code Review.
* [24. Changelog](24_changelog.md) — Catatan Perubahan Versi Platform Berbasis Semantic Versioning (SemVer).

---

## 🏗️ Filosofi Rekayasa Kita

Sebagai tim startup yang membangun produk *enterprise-ready*, kita memegang teguh prinsip-prinsip berikut dalam setiap baris kode yang kita commit:
1.  **Keputusan yang Dapat Dijelaskan (Decision Intelligence)**: Kita tidak hanya merekam data inventaris. Platform kita wajib memberikan rekomendasi aksi nyata yang dilengkapi dengan penjelasan konteks bisnis.
2.  **Isolasi Multi-Tenant Mutlak**: Keamanan data klien dilindungi langsung di level kernel database menggunakan PostgreSQL Row-Level Security (RLS). Kebocoran data antar penyewa adalah toleransi nol (*zero tolerance*).
3.  **Kualitas Produksi Sejak Hari Pertama**: Kita tidak menulis kode asal jadi. Pola *Repository Pattern*, *Dependency Injection*, *Strong Typing*, dan pengujian otomatis wajib diimplementasikan sejak awal.

---
*Dokumentasi ini bersifat rahasia dan merupakan hak milik intelektual StockSense AI Startup.*