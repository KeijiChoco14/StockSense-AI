# 02. Product Requirement Document (PRD) - MVP Scope

## 1. Status Dokumen & Kontrol Versi
- **Target Rilis**: MVP (Minimum Viable Product) v1.0.0
- **Penulis**: Technical Co-Founder & Product Team
- **Status**: APPROVED / READY FOR DEVELOPMENT

## 2. Cakupan Fitur Utama MVP (Fitur Inti)
Untuk rilis pertama, platform difokuskan pada tiga modul pilar yang menyelesaikan masalah *inventory management* secara end-to-end:

### Modul A: Multi-Tenant Inventory Control
*   **A.1 Ledger Stok Real-Time**: Pencatatan mutasi stok keluar-masuk (Penjualan, Restock, Wastage/Rusak) dengan presisi tingkat desimal ($12, 4$).
*   **A.2 Manajemen SKU Bahan Baku**: Pengelompokan berdasarkan kategori, satuan unit ($UoM$), harga beli rata-rata, dan lokasi penyimpanan (Chiller, Gudang Kering).
*   **A.3 Threshold Stok Kritis**: Notifikasi otomatis berbasis *Safety Stock* manual yang ditentukan oleh pengguna sebelum sistem AI mengambil alih secara otomatis.

### Modul B: AI-Driven Demand & Stockout Forecasting
*   **B.1 Prediksi Tingkat Kehabisan Stok**: Menghitung metrik *Days Until Stockout* untuk setiap bahan baku sensitif.
*   **B.2 Estimasi Penjualan Prediktif**: Memprediksi volume pemakaian bahan baku untuk 7 hari ke depan dengan mempertimbangkan tren musiman (misal: akhir pekan).
*   **B.3 Panel Asisten AI (Explainable AI)**: Menyediakan teks naratif pendek yang menjelaskan *mengapa* bahan tersebut harus dibeli (misal: "Tren menu Latte naik 20%").

### Modul C: Automated Procurement Workflow
*   **C.1 Generator Draft Purchase Order (PO)**: Membuat draf pesanan otomatis yang berisi daftar barang yang kritis beserta kuantitas rekomendasi dari AI.
*   **C.2 Manajemen Supplier**: Database vendor lengkap dengan informasi kontak, batas minimum order, dan *lead time* pengiriman bawaan.
*   **C.3 Alur Persetujuan PO**: Status PO berjenjang mulai dari `Draft` -> `Pending Approval` -> `Sent` -> `Received` -> `Partially Received`.

---

## 3. Matriks Maturitas & Batasan Fitur (Out of Scope untuk MVP)
Agar pengembangan fokus dan rilis tepat waktu, fitur-fitur berikut ditangguhkan ke Fase 2:
*   Integrasi otomatis API POS pihak ketiga secara komprehensif (MVP menggunakan fitur *mock import data sales via CSV*).
*   Multi-warehouse/Transfer stok antar outlet cabang (MVP hanya mendukung 1 tenant = 1 lokasi utama).
*   Model AI kustomisasi per cuaca atau event kalender makro nasional.

## 4. Kriteria Kelayakan Rilis (Release Criteria)
*   **Kinerja Efisiensi**: Operasi baca data (Read) untuk dasbor utama wajib berada di bawah 200ms pada kondisi jaringan normal.
*   **Ketahanan Isolasi Data**: Pengujian penetrasi internal harus membuktikan bahwa User Tenant A tidak dapat mengakses baris data milik Tenant B dengan memanipulasi parameter query API (*Zero Cross-Tenant Leakage*).