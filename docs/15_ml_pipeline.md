# 15. ML Pipeline & Time-Series Forecasting

Dokumen ini menjelaskan alur siklus hidup data, rekayasa fitur, spesifikasi arsitektur model Deep Learning, serta strategi menangani data baru (Cold Start).

---

## 1. Arsitektur Model: Gated Recurrent Unit (GRU)

Untuk memprediksi volume kebutuhan stok bahan baku berbasis data deret waktu harian, kita menggunakan arsitektur TensorFlow/Keras GRU. GRU dipilih karena performanya yang setara dengan LSTM dalam menangkap ketergantungan jangka panjang (long-term dependencies) namun memiliki waktu komputasi yang jauh lebih cepat karena struktur gerbang (gate) yang lebih efisien.

### Struktur Layer Model:
- Input Layer: Menerima matriks tensor 3 dimensi dengan bentuk: [batch_size, time_steps, feature_count]. MVP menggunakan window ukuran time_steps = 30 (30 hari historis penjualan).
- GRU Layer 1: 64 Units, dilengkapi dengan return_sequences=True untuk meneruskan urutan data ke layer berikutnya.
- Dropout Layer: Tingkat drop 0.2 untuk mencegah terjadinya overfitting pada tren lokal.
- GRU Layer 2: 32 Units, return_sequences=False (hanya mengambil output status akhir).
- Dense Output Layer: 1 Unit dengan fungsi aktivasi Linear (karena kita memprediksi nilai kontinu berupa kuantitas bahan baku).

---

## 2. Strategi Mengatasi Cold Start Problem

Cold Start terjadi ketika ada tenant baru yang mendaftar ke platform, atau ketika tenant meluncurkan item menu dan bahan baku baru yang belum memiliki data riwayat mutasi historis sama sekali.

### Protokol Penanganan Cold Start di StockSense AI:
- Fase 0 - 7 Hari Pertama: Sistem menggunakan parameter batas aman manual (Safety Stock Threshold) yang ditentukan sendiri oleh pengguna sebagai acuan utama sistem peringatan dini.
- Fase Hari ke-8 hingga ke-29: Sistem mengaktifkan model prediksi statistik sederhana (Rata-rata bergerak linear / Moving Average) yang diperbarui setiap malam.
- Fase Hari ke-30 dan Seterusnya: Sistem secara otomatis mengalihkan mesin komputasi ke Model Prediksi GRU Deep Learning secara penuh karena jendela data historis minimal (30 hari) telah terpenuhi.