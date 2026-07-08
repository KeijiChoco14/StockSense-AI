# 11. Database Design & Schema Specification

Desain database PostgreSQL untuk StockSense AI dirancang dengan fondasi multi-tenant yang kuat, audit log mutlak, pengamanan integritas data, dan indexing agresif pada kolom query frekuensi tinggi.

---

## 1. Konvensi Tabel Umum (Global Columns)

Setiap tabel di dalam sistem StockSense AI (kecuali tabel `tenants`) WAJIB memiliki kolom-kolom struktural dasar berikut untuk mempermudah pelacakan audit dan isolasi data:

* **`id`**: `UUID` (Primary Key, menggunakan fungsi bawaan `gen_random_uuid()` untuk mencegah enumerasi ID oleh pihak luar).
* **`tenant_id`**: `UUID` (Foreign Key ke tabel `tenants` dengan aksi `ON DELETE CASCADE`. Kolom ini menjadi jangkar utama untuk Row-Level Security).
* **`created_at`**: `TIMESTAMPTZ` (Default `NOW()`, merekam waktu data pertama kali dibuat menggunakan zona waktu standar UTC).
* **`updated_at`**: `TIMESTAMPTZ` (Default `NOW()`, diperbarui otomatis via database trigger setiap terjadi operasi `UPDATE`).
* **`deleted_at`**: `TIMESTAMPTZ` (Nullable. Jika berisi nilai waktu, data dianggap terhapus secara logis/*Soft Delete* dan otomatis diabaikan oleh query standar aplikasi).

---

## 2. Definisi Skema Core Tables (SQL DDL)

Berikut adalah skrip DDL murni PostgreSQL untuk pembentukan tabel-tabel utama di fase MVP:

```sql
-- 1. TABEL TENANTS (Penyewa Utama / Perusahaan)
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL,
    subscription_tier VARCHAR(50) NOT NULL DEFAULT 'growth',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. TABEL USERS (Pengguna Sistem)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'staff',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uk_tenant_user_email UNIQUE (tenant_id, email)
);

-- 3. TABEL INGREDIENTS (Daftar Bahan Baku Inventaris)
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    current_stock NUMERIC(12, 4) NOT NULL DEFAULT 0.0000,
    safety_stock NUMERIC(12, 4) NOT NULL DEFAULT 0.0000,
    unit_of_measure VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uk_tenant_ingredient_sku UNIQUE (tenant_id, sku)
);