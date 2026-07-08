# 21. Deployment Architecture & CI/CD GitOps Pipeline

StockSense AI mengadopsi metodologi GitOps yang terautomasi penuh dari repositori GitHub hingga lingkungan produksi (Production Environment).

---

## 1. Infrastruktur Server & Hosting Target

- Backend Server: Menggunakan aplikasi FastAPI yang dibungkus ke dalam container Docker dan di-deploy ke platform cloud Railway dengan strategi penskalaan horizontal otomatis (auto-scaling).
- Frontend Web App: Aplikasi Next.js 15 di-deploy langsung ke infrastruktur Vercel Edge Network untuk menjamin latensi rendering antarmuka yang optimal di seluruh dunia.
- Database Cloud: Menggunakan kluster database PostgreSQL terkelola (Managed Database Cluster) yang dilengkapi dengan replikasi cadangan otomatis harian.

---

## 2. Alur Kerja Pipa CI/CD (GitHub Actions Workflow)

Setiap kali developer melakukan operasi git push atau membuka Pull Request ke cabang main, pipa otomatis GitHub Actions akan terpicu secara berurutan:

- Tahap 1: Linter & Formatter — Menjalankan Ruff (Python) & ESLint (TypeScript) untuk memvalidasi kerapian penulisan kode.
- Tahap 2: Automated Testing — Eksekusi PyTest Unit & Integration di Server CI. Harus lolos 100% dan memenuhi batas minimum cakupan kode.
- Tahap 3: Build Container — Mengompilasi Docker Image baru jika seluruh tes lulus dan mengirimkannya ke Container Registry aman.
- Tahap 4: Auto-Deploy — Memicu pembaruan container secara instan di Railway untuk Backend dan pembaruan build di Vercel untuk Frontend.