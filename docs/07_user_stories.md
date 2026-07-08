# 07. User Stories

Seluruh backlog pengembangan fitur StockSense AI didorong oleh User Stories yang berfokus pada penyampaian nilai nyata operasional restoran (*User-Centric Value*).

---

## Epic 1: Multi-Tenant Ledger & Inventory Management
* **US-101 (Stok Real-Time)**: Sebagai Restaurant Manager, saya ingin melihat daftar stok bahan baku yang diperbarui secara otomatis setiap kali ada penjualan menu, sehingga saya tidak perlu melakukan perhitungan fisik setiap jam.
* **US-102 (Soft Delete & Audit Log)**: Sebagai Pemilik Restoran, saya ingin setiap koreksi stok yang dilakukan oleh staf gudang tercatat alasan dan identitas pengubahnya ke dalam sistem tak terubah (*immutable log*), untuk meminimalkan risiko manipulasi data dan kecurangan internal.
* **US-103 (Multi-Unit Conversion)**: Sebagai Staf Purchasing, saya ingin dapat memasukkan data pembelian bahan baku dalam satuan grosir (misal: Dus/Kardus) namun otomatis terurai menjadi satuan operasional dapur (misal: Gram/Mililiter) berdasarkan konfigurasi resep, agar kalkulasi stok presisi.

---

## Epic 2: AI Forecasting & Decision Intelligence
* **US-201 (Days Until Stockout)**: Sebagai Restaurant Manager, saya ingin sistem menampilkan metrik sisa hari sebelum barang habis untuk setiap SKU, sehingga saya dapat menyusun prioritas pemesanan barang sebelum kehabisan stok.
* **US-202 (Explainable AI Recommendations)**: Sebagai Pemilik Jaringan Restoran, saya ingin rekomendasi jumlah pembelian yang dihasilkan oleh AI disertai dengan penjelasan tekstual mengenai faktor penyebabnya (seperti tren penjualan atau performa supplier), agar tim manajer saya percaya dan bersedia mengeksekusi rekomendasi tersebut.

---

## Epic 3: Procurement Automation Workflow
* **US-301 (Auto-Generate Draft PO)**: Sebagai Staf Purchasing, saya ingin sistem otomatis membuat draf Purchase Order yang sudah terisi kuantitas optimal saat stok menyentuh batas aman (*Safety Stock*), sehingga saya tidak perlu membuat dokumen PO dari awal menggunakan program teks manual.
* **US-302 (Supplier Performance Tracking)**: Sebagai Group CFO, saya ingin melihat peringkat performa supplier berdasarkan akurasi kuantitas pengiriman barang dan stabilitas harga historis, sehingga saya memiliki posisi tawar yang kuat saat melakukan negosiasi kontrak tahunan.

---

## Epic 4: Kitchen Waste Control & Expiry Matrix
* **US-401 (FEFO Expiry Dashboard)**: Sebagai Head Chef, saya ingin melihat daftar bahan baku yang mendekati masa kedaluwarsa dalam 48 jam ke depan di layar tablet dapur, sehingga saya dapat menginstruksikan tim juru masak untuk memprioritaskan pemakaian bahan tersebut pada menu harian.