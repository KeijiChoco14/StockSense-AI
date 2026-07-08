# 06. User Journey Map

## Perjalanan Pengguna: Amelia Putri (Restaurant General Manager) dalam Siklus Pengisian Stok

Dokumen ini memetakan bagaimana StockSense AI mentransformasi pengalaman operasional manajer restoran dari proses manual yang reaktif menjadi ekosistem digital yang proaktif.

---

## 1. Peta Perjalanan Pengguna (User Journey Table)

| Tahapan (Phase) | 1. Discovery (Penemuan Risiko) | 2. Evaluation (Penilaian AI) | 3. Action (Eksekusi PO) | 4. Closing Loop (Penerimaan) |
| :--- | :--- | :--- | :--- | :--- |
| **Aktivitas Pengguna** | Membuka dasbor pagi hari dan melihat notifikasi stok kritis. | Meninjau grafik prediksi dan membaca narasi penjelasan AI (XAI). | Menyetujui draf Purchase Order (PO) otomatis dan mengirimkannya ke vendor. | Memeriksa fisik barang yang datang dan melakukan input *check-in* kuantitas. |
| **Sistem Respons** | Menghitung metrik *Days Until Stockout* secara real-time. | Menyajikan argumen logis berbasis tren penjualan historis dan *lead time*. | Mengunci log transaksi, membuat PDF PO formal, dan mengirim notifikasi via email/WA. | Memperbarui angka *current stock* secara instan dan menyinkronkan data harga terbaru. |
| **Skor Pengalaman** | 😊 **Tinggi (4/5)** | 🤩 **Sangat Tinggi (5/5)** | 🤩 **Sangat Tinggi (5/5)** | 😊 **Tinggi (4/5)** |
| **Konteks Emosional** | Tenang karena diingatkan lebih awal sebelum stok benar-benar habis. | Percaya diri dengan keputusan karena AI memberikan alasan yang masuk akal. | Sangat puas karena menghemat waktu administrasi hingga 90%. | Lega karena sistem langsung menghitung pembaruan COGS secara otomatis. |

---

## 2. Alur Diagram Arus Kerja (Workflow Diagram)

Berikut adalah visualisasi alur perpindahan data dan keputusan dari deteksi awal hingga pengisian stok selesai:

[Mulai: Dasbor Utama]
        │
        ▼
 (Notifikasi Stok Kritis) ──► Sistem mendeteksi sisa hari bahan baku (Days Until Stockout)
        │
        ▼
 [Review AI Recommendation] ──► Pengguna membaca penjelasan kontekstual AI (XAI)
        │
        ▼
   (Setujui Draf PO?) 
   ├──► TIDAK: Sesuaikan kuantitas manual
   └──► YA: Klik "Approve & Send"
        │
        ▼
 [Sistem Kirim PO ke Vendor] ──► Status berubah menjadi 'Sent' (PDF dikirim otomatis)
        │
        ▼
 [Penerimaan Barang di Gudang] ──► Staf input kuantitas aktual yang diterima
        │
        ▼
[Selesai: Stok Diperbarui] ──► Angka stok naik & data harga masuk ke kalkulasi COGS

---

## 3. Titik Kontak Utama (Touchpoints) & Peluang Optimasi

*   **Touchpoint 1: Mobile App Widget / Push Notification**
    *   *Masalah Tradisional*: Manajer baru tahu barang habis saat koki berteriak di dapur.
    *   *Solusi StockSense AI*: Notifikasi proaktif dikirimkan 72 jam sebelum prediksi kehabisan stok terjadi berdasarkan analisis tren konsumsi.
*   **Touchpoint 2: Panel Asisten AI (Explainable AI)**
    *   *Masalah Tradisional*: Pengguna sering mengabaikan rekomendasi sistem otomatis karena tidak tahu dasar perhitungannya.
    *   *Solusi StockSense AI*: Menghilangkan fenomena *black box* dengan menuliskan alasan logis seperti: *"Rekomendasi 40kg didasarkan pada lonjakan menu Iced Latte sebesar 20% setiap akhir pekan."*