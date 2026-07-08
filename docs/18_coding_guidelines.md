# 18. Coding Guidelines & Engineering Standards

Seluruh tim rekayasa perangkat lunak StockSense AI wajib mematuhi standar penulisan kode berikut demi menjaga keterbacaan, skalabilitas, dan kemudahan proses peninjauan kode (Code Review).

---

## 1. Standar Python Backend (FastAPI Async)

- Asynchronous-First: Seluruh endpoint API, pemanggilan repositori database, dan komunikasi jaringan WAJIB ditulis menggunakan fungsi asinkron (async def) dan menyertakan kata kunci await.
- Strong Typing Obligation: Kami melarang penggunaan tipe data dinamik implisit. Setiap argumen fungsi dan nilai kembalian wajib dideklarasikan tipenya secara eksplisit (Python Type Hints).

### Aturan Struktur Penulisan Kode Service:
- Penggunaan dependency injection yang jelas melalui constructor (__init__).
- Validasi data dasar wajib dilakukan sebelum memanggil lapisan data layer / repository.
- Error handling menggunakan custom HTTP exceptions bawaan FastAPI agar response status code akurat.

---

## 2. Standar TypeScript Frontend (Next.js 15)

- App Router: Proyek frontend menggunakan arsitektur folder Next.js App Router (/app).
- Server Components by Default: Seluruh komponen pembentuk halaman secara bawaan adalah React Server Components (RSC). Deklarasi "use client" hanya disematkan pada komponen tingkat terbawah yang membutuhkan interaktivitas langsung (seperti tombol klik, penanganan form, atau grafik interaktif).