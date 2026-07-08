# 20. Testing Strategy & Automated QA Quality Gates

Kualitas kode dijamin oleh piramida pengujian otomatis yang ketat. Setiap pengajuan Pull Request wajib melewati batas minimum kelulusan tes (Quality Gate) sebelum diizinkan masuk ke cabang utama (main).

---

## 1. Struktur Piramida Pengujian (Testing Pyramid Target)

- Unit Tests (Cakupan Target: 80%+): Pengujian unit fokus pada validasi fungsi logika murni di lapisan Domain dan Service tanpa menyentuh koneksi database asli atau server luar (menggunakan Mocking).
- Integration Tests (Cakupan Target: 15%): Pengujian integrasi memastikan FastAPI Router dapat berkomunikasi dengan benar ke PostgreSQL melalui repositori async. Tes ini dijalankan di dalam container database terisolasi menggunakan pustaka Docker Testcontainers.
- End-to-End (E2E) Tests (Cakupan Target: 5%): Pengujian antarmuka dari ujung ke ujung menggunakan kerangka kerja Playwright untuk mensimulasikan alur klik pengguna riil pada browser.

---

## 2. Parameter Kelulusan (Quality Gates)

Setiap kode baru yang dimasukkan ke repositori harus memenuhi kriteria berikut:
- Seluruh rangkaian pengujian (test suite) harus berstatus lulus (100% green).
- Cakupan pengujian kode baru tidak boleh menurunkan persentase akumulatif cakupan pengujian global (global coverage code).
- Hasil pemindaian kode otomatis (Linter) tidak boleh mendeteksi adanya celah keamanan kritis atau pelanggaran gaya penulisan kode standar.