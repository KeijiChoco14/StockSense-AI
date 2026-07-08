# 19. Security Architecture & Isolation Protocols

Keamanan data pelanggan adalah prioritas mutlak di StockSense AI. Arsitektur keamanan kami dirancang untuk mencegah kebocoran data antar tenant (cross-tenant data leaks) dan mengamankan transmisi data.

---

## 1. Protokol Autentikasi JWT Berdurasi Ketat

- Otentikasi pengguna divalidasi menggunakan token JWT (JSON Web Token) yang dikirim melalui header HTTP `Authorization: Bearer <TOKEN>`.
- Algoritma enkripsi tanda tangan yang diwajibkan adalah HS256.
- Masa Berlaku Token Access: Dibatasi maksimal selama 15 menit semenjak waktu diterbitkan.
- Masa Berlaku Token Refresh: Dibatasi maksimal selama 7 hari, disimpan dengan aman di dalam cookie browser yang terenkripsi dengan atribut keamanan penuh: `HttpOnly`, `Secure`, dan `SameSite=Strict`.

---

## 2. Isolasi Baris Data Database (PostgreSQL Row-Level Security)

Untuk memastikan kesalahan logika kode di backend tidak mengakibatkan kebocoran data milik tenant lain, kami menerapkan gerbang keamanan ganda langsung di dalam mesin database PostgreSQL menggunakan fitur Row-Level Security (RLS).

### Mekanisme Kerja Sesi di Backend (FastAPI Middleware):
Setiap kali ada request HTTP masuk, middleware FastAPI mengekstrak `tenant_id` dari token JWT pengguna, kemudian menjalankan perintah SQL pembuka sesi sebelum mengeksekusi query bisnis utama:
- Sistem menetapkan parameter lokal sesi database (`SET LOCAL app.current_tenant_id = 'id-tenant'`).
- Mesin PostgreSQL secara otomatis memblokir atau menyaring baris data apa pun yang tidak sesuai dengan ID tenant aktif tersebut.
- Mekanisme ini menjamin keamanan isolasi data murni di level basis data, bahkan jika developer tidak sengaja melewatkan klausa filter WHERE pada kode program.