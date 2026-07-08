# 16. UI Guidelines & Aesthetics Philosophy

StockSense AI mengusung filosofi desain antarmuka premium sekelas aplikasi produktivitas elit modern (seperti Linear, Stripe, dan Vercel). Kami berfokus pada kejelasan informasi, kerapian visual, kontras tinggi, dan efisiensi navigasi keyboard.

---

## 1. Karakteristik Estetika Desain (Premium Aesthetics)

- Minim Dekorasi, Maksimalkan Kontras: Kami menghindari gradasi warna cerah yang berlebihan atau bayangan dekoratif yang tebal. Kedalaman visual dibentuk menggunakan garis tepi tipis berwarna abu-abu netral (Subtle Borders) dan penggunaan latar belakang gelap/terang monokromatik yang solid.
- Tipografi Berbasis Data: Informasi angka, desimal stok, dan status kritis adalah pusat perhatian utama sistem. Font monospace digunakan khusus untuk penyajian angka agar susunan tabel tetap sejajar rapi saat dibaca cepat.
- Informasi Berdensitas Tinggi (High-Density Displays): Antarmuka dirancang untuk meminimalkan ruang kosong yang sia-sia (whitespace optimization). Admin gudang dan manajer operasional harus dapat melihat puluhan data SKU sekaligus tanpa perlu terlalu banyak menggulir halaman (scrolling).

---

## 2. Aturan Navigasi & Kecepatan Kerja

Aplikasi harus dioptimalkan untuk pengoperasian tanpa mouse (keyboard-first navigation):
- Pencarian global universal (Command Pallete) dapat diakses instan melalui kombinasi tombol CMD + K atau CTRL + K.
- Tabel data besar wajib memiliki fitur navigasi panah keyboard atas-bawah untuk berpindah baris, serta tombol enter untuk membuka detail baris.