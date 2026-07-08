# 23. Contributing Guidelines & Git Branching Strategy

Selamat datang di tim rekayasa StockSense AI! Untuk menjaga kerapian dan stabilitas cabang kode utama kami, seluruh kontributor wajib mengikuti protokol Git Flow yang disepakati bersama.

---

## 1. Strategi Pencabangan Git (Git Branching Strategy)

Kami melarang keras pengembang melakukan commit perubahan kode secara langsung ke cabang main. Setiap pekerjaan fitur baru atau perbaikan bug harus dilakukan di cabang terisolasi menggunakan konvensi nama berikut:

- Fitur Baru: feature/nama-fitur-singkat (Contoh: feature/inventory-ledger-api).
- Perbaikan Bug: bugfix/deskripsi-pendek-bug (Contoh: bugfix/jwt-expiration-timezone).
- Optimasi Performa: perf/bagian-yang-dioptimasi (Contoh: perf/database-index-ingredients).

---

## 2. Aturan Format Pesan Commit (Conventional Commits)

Pesan commit wajib ditulis dalam format yang terstruktur dengan jelas agar riwayat pelacakan git dapat menghasilkan catatan perubahan (Changelog) otomatis:

Format: <tipe>(<lingkup-modul>): <deskripsi singkat kalimat imperatif masa kini>

Contoh Pesan Commit yang Valid:
- feat(inventory): add async repository pattern for bulk insert raw ingredients
- fix(auth): resolve token refresh invalid signature validation error during midnight
- docs(readme): update system deployment architectural topology infrastructure description