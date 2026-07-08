# 08. Functional Requirements & Business Rules

Dokumen ini mendefinisikan seluruh fungsionalitas sistem yang wajib diimplementasikan pada StockSense AI MVP beserta aturan bisnis yang mengikatnya.

---

## 1. Modul Manajemen Inventaris (Inventory Management)

### FR-101: Pencatatan Mutasi Stok Berbasis Ledger
*   **Deskripsi**: Setiap perubahan stok (penambahan atau pengurangan) tidak boleh langsung mengubah kolom total secara kasar, melainkan wajib dicatat sebagai baris mutasi baru di tabel ledger stok.
*   **Aturan Bisnis**:
    *   Setiap baris mutasi harus memiliki tipe transaksi yang jelas: `SALES` (pengurangan otomatis via POS), `PURCHASE` (penambahan via PO), `WASTAGE` (bahan rusak/busuk), atau `ADJUSTMENT` (koreksi stok fisik).
    *   Nilai kuantitas mutasi disimpan dalam tipe data desimal presisi tinggi (4 angka di belakang koma) untuk mengakomodasi bahan baku mikro seperti bumbu atau esensial oil.

### FR-102: Validasi Stok Multi-Tenant (Isolasi Data)
*   **Deskripsi**: Sistem harus menjamin bahwa pengguna hanya dapat melihat, menambah, atau mengubah data inventaris yang memiliki ID Tenant yang sama dengan ID Tenant pengguna tersebut.
*   **Aturan Bisnis**: Filter `tenant_id` wajib diterapkan di setiap query database (ditegaskan di level database menggunakan PostgreSQL Row-Level Security).

---

## 2. Modul Prediksi AI (AI Forecasting Engine)

### FR-201: Kalkulasi Metrik Days Until Stockout
*   **Deskripsi**: Sistem harus menghitung sisa waktu (dalam satuan hari) sebelum suatu bahan baku habis total berdasarkan volume stok saat ini dibagi dengan rata-rata tingkat konsumsi harian prediktif.
*   **Aturan Bisnis**:
    *   Kalkulasi dilakukan secara otomatis setiap kali ada data penjualan baru yang masuk atau minimal 1 kali sehari melalui *cron job* terjadwal.
    *   Jika nilai *Days Until Stockout* kurang dari atau sama dengan 3.0 hari, sistem wajib menaikkan status SKU tersebut menjadi `CRITICAL` di halaman dasbor.

### FR-202: Generasi Narasi Explainable AI (XAI)
*   **Deskripsi**: Sistem harus menampilkan teks penjelasan dalam bahasa alami yang menerangkan alasan di balik angka rekomendasi pembelian yang diajukan oleh model machine learning.
*   **Aturan Bisnis**: Narasi harus menggabungkan variabel data riil, seperti persentase kenaikan tren penjualan produk terkait pada akhir pekan, atau riwayat keterlambatan pengiriman oleh supplier.

---

## 3. Modul Alur Kerja Pembelian (Procurement Workflow)

### FR-301: Pembuatan Otomatis Draf Purchase Order (PO)
*   **Deskripsi**: Ketika sebuah bahan baku masuk ke status `CRITICAL`, sistem harus menyediakan fungsi satu klik untuk membuat draf dokumen Purchase Order (PO).
*   **Aturan Bisnis**:
    *   Sistem otomatis memilih supplier utama yang terikat dengan SKU tersebut.
    *   Kuantitas pesanan awal diisi otomatis menggunakan angka rekomendasi optimal dari AI (menyeimbangkan *safety stock* dan batas minimum order vendor).

### FR-302: Alur Persetujuan Berjenjang (PO State Machine)
*   **Deskripsi**: Dokumen PO harus melewati siklus hidup status yang ketat sebelum stok di gudang resmi bertambah.
*   **Aturan Bisnis**:
    *   Status awal adalah `DRAFT` (bisa diubah oleh staf).
    *   Berubah menjadi `PENDING_APPROVAL` saat diajukan ke manajer.
    *   Berubah menjadi `SENT` setelah disetujui dan sistem mengirimkan PDF ke vendor.
    *   Berubah menjadi `RECEIVED` atau `PARTIALLY_RECEIVED` saat barang fisik sampai di gudang dan diverifikasi oleh staf. Hanya pada status inilah *current stock* di ledger akan bertambah.