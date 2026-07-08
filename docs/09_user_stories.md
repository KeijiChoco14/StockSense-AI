# 09. User Stories & Persona Matrix

Dokumen ini mendefinisikan karakteristik pengguna utama platform StockSense AI serta skenario kebutuhan nyata (user stories) yang menjadi dasar pengembangan fitur sistem.

---

## 1. Matriks Persona Pengguna

### Persona A: Owner / Pemilik Bisnis (Budi Santoso)
- Karakteristik: Pemilik jaringan restoran waralaba 3 cabang, fokus pada profitabilitas keseluruhan, efisiensi biaya, dan laporan eksekutif.
- Masalah Utama: Sering terjadi kebocoran biaya operasional akibat bahan baku kedaluwarsa atau hilang di gudang cabang tanpa pelacakan terpusat.

### Persona B: Manajer Operasional / Dapur (Siti Aminah)
- Karakteristik: Bertanggung jawab atas ketersediaan stok harian di dapur utama, kualitas bahan, dan hubungan dengan vendor penyuplai.
- Masalah Utama: Menghabiskan waktu 2 jam setiap malam hanya untuk menghitung sisa stok secara manual dan menebak-nebak jumlah order untuk hari berikutnya.

---

## 2. Daftar User Stories MVP

Setiap fungsionalitas sistem wajib mengacu pada salah satu user story di bawah ini demi menjaga fokus pengembangan:

### Kelompok Fitur: Autentikasi & Multi-Tenancy
- **STORY-01**: Sebagai seorang Pemilik Bisnis, saya ingin mendaftarkan perusahaan saya ke dalam platform sehingga saya bisa mendapatkan ruang kerja digital (tenant) yang terisolasi dan aman untuk seluruh staf saya.
- **STORY-02**: Sebagai seorang Manajer Operasional, saya ingin masuk ke sistem menggunakan email dan kata sandi yang aman agar data inventaris restoran kami tidak dapat diakses oleh pihak luar.

### Kelompok Fitur: Manajemen Inventaris (Core Ledger)
- **STORY-03**: Sebagai seorang Manajer Operasional, saya ingin mendaftarkan SKU bahan baku baru beserta ambang batas aman (safety stock), sehingga sistem bisa memberikan peringatan jika stok mulai menipis.
- **STORY-04**: Sebagai seorang Staf Gudang, saya ingin mencatat mutasi stok masuk dan keluar dengan mudah agar saldo akhir bahan baku di dasbor selalu akurat (real-time).

### Kelompok Fitur: Prediksi AI & Pembuatan Order
- **STORY-05**: Sebagai seorang Manajer Operasional, saya ingin melihat rekomendasi jumlah pembelian bahan baku yang dihitung otomatis oleh AI, sehingga saya tidak perlu menebak-nebak orderan dan bisa menghindari risiko kehabisan stok (stockout).