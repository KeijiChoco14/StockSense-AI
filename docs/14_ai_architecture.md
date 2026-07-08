# 14. AI Architecture & Explainable AI (XAI) Framework

StockSense AI bukan sekadar alat pencatat; platform ini dirancang sebagai Decision Intelligence Engine. Arsitektur AI kami berfokus pada akurasi prediksi sekaligus transparansi keputusan bisnis.

---

## 1. Komponen Utama Decision Intelligence

Sistem kecerdasan buatan kami dibagi menjadi tiga komponen logis yang bekerja berurutan:

1. Data Ingestion Hub: Mengumpulkan sinyal-sinyal data mentah dari modul log transaksi POS, logistik eksternal, dan mutasi ledger inventaris historis.
2. Predictive Model (GRU Core): Jaringan saraf berulang (Gated Recurrent Unit) yang memproses urutan deret waktu (time-series) untuk memproyeksikan volume konsumsi bahan baku di masa depan.
3. Explainable Narrative Generator (XAI): Mesin penerjemah berbasis aturan template linguistik bisnis yang mengonversi bobot matriks keputusan AI menjadi narasi teks logis yang dapat dipahami manusia.

---

## 2. Framework Transparansi (Explainable AI Engine)

Kami sangat menentang model kecerdasan buatan berbentuk Black Box (kotak hitam tersembunyi) yang hanya menyajikan angka keluaran kasar tanpa argumen pendukung. Pengguna lapangan tidak akan mempercayai rekomendasi order jika mereka tidak tahu dari mana asal angka tersebut.

### Skema Logika Generasi Narasi XAI:
Sistem menggunakan mesin inferensi berbasis logika bersyarat untuk merangkai string teks secara dinamis berdasarkan data metrik aktual:

- Kondisi Metrik Penjualan: Jika tren konsumsi menu berelasi naik > 15% seminggu terakhir.
- Kondisi Lead Time Vendor: Jika deviasi pengiriman supplier utama melambat > 1.5 hari.

Output Narasi Teks yang Ditampilkan di UI Dashboard:
"AI merekomendasikan order sebanyak X kg karena penjualan menu terkait naik 18% menjelang akhir pekan, serta mengantisipasi keterlambatan kirim vendor sebesar 1.5 hari."