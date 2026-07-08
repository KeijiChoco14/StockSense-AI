# 12. Entity Relationship Diagram (ERD) & Data Dictionary

Dokumen ini mendefinisikan hubungan struktural antar entitas data di dalam StockSense AI, aturan integritas referensial (cascade rules), serta kamus data terperinci untuk tabel core sistem.

---

## 1. Arsitektur Hubungan Entitas (ERD Layout)

Seluruh tabel operasional dalam sistem StockSense AI terikat secara struktural ke tabel jangkar `tenants`. Hal ini memastikan bahwa data terisolasi secara logis dari level database yang paling mendasar.

[Mulai: Tenants]
        │
        ├───(1:N)───► [USERS]
        │
        ├───(1:N)───► [INGREDIENTS]
        │
        └───(1:N)───► [PURCHASE_ORDERS]

### Aturan Relasi Mutlak (Referential Integrity Rules):
* **tenants to users (1:N)**: Satu perusahaan (tenant) dapat memiliki banyak pengguna (users). Jika sebuah tenant dihapus dari sistem, seluruh data user yang terikat wajib terhapus otomatis (ON DELETE CASCADE).
* **tenants to ingredients (1:N)**: Satu tenant memiliki daftar bahan bakunya tersendiri. SKU bahan baku hanya bersifat unik di dalam lingkup ID Tenant yang sama (UNIQUE(tenant_id, sku)).

---

## 2. Kamus Data Terperinci (Data Dictionary)

### Tabel A: tenants
Menyimpan informasi badan usaha atau badan hukum klien yang berlangganan platform StockSense AI.

- id (UUID): Primary Key, Default gen_random_uuid(). Identifikasi unik global untuk setiap penyewa (Tenant).
- company_name (VARCHAR(255)): NOT NULL. Nama resmi perusahaan atau brand restoran klien.
- subscription_tier (VARCHAR(50)): NOT NULL, Default 'growth'. Tingkatan paket layanan (growth, enterprise).
- created_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu registrasi tenant ke dalam platform (UTC).
- updated_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu perubahan terakhir data profil tenant (UTC).

### Tabel B: users
Menyimpan data kredensial, profil, dan peran hak akses (RBAC) bagi personel pengguna platform.

- id (UUID): Primary Key, Default gen_random_uuid(). Identifikasi unik untuk setiap individu pengguna.
- tenant_id (UUID): Foreign Key, NOT NULL. Menghubungkan user ke entitas tenants.id.
- email (VARCHAR(255)): NOT NULL. Alamat email unik untuk login di dalam tenant terkait.
- hashed_password (VARCHAR(255)): NOT NULL. String kata sandi yang telah diamankan via algoritma Bcrypt.
- full_name (VARCHAR(255)): NOT NULL. Nama lengkap pengguna untuk keperluan display UI.
- role (VARCHAR(50)): NOT NULL, Default 'staff'. Tingkatan akses pengguna (owner, manager, staff).
- is_active (BOOLEAN): NOT NULL, Default TRUE. Status penanda apakah user diizinkan mengakses sistem.
- created_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu akun user berhasil dibuat (UTC).
- updated_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu perubahan terakhir data profil user (UTC).
- deleted_at (TIMESTAMPTZ): Nullable. Cap waktu penghapusan logis (Soft Delete).

### Tabel C: ingredients
Menyimpan daftar master bahan baku inventaris yang digunakan di operasional dapur.

- id (UUID): Primary Key, Default gen_random_uuid(). Identifikasi unik untuk setiap item bahan baku.
- tenant_id (UUID): Foreign Key, NOT NULL. Menghubungkan bahan ke entitas tenants.id.
- sku (VARCHAR(100)): NOT NULL. Stock Keeping Unit / Kode unik bahan (misal: RAW-MILK-01).
- name (VARCHAR(255)): NOT NULL. Nama komersial bahan baku (misal: Susu Segar 1L).
- category (VARCHAR(100)): NOT NULL. Kategori pengelompokan bahan (misal: Dairy, Meat).
- current_stock (NUMERIC(12, 4)): NOT NULL, Default 0.0000. Saldo stok fisik riil saat ini di gudang.
- safety_stock (NUMERIC(12, 4)): NOT NULL, Default 0.0000. Batas minimum stok aman sebelum status jadi kritis.
- unit_of_measure (VARCHAR(50)): NOT NULL. Satuan ukuran stok gudang (misal: kg, liter, pcs).
- created_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu item bahan baku pertama kali didaftarkan (UTC).
- updated_at (TIMESTAMPTZ): NOT NULL, Default NOW(). Waktu perubahan terakhir pada data item bahan (UTC).
- deleted_at (TIMESTAMPTZ): Nullable. Cap waktu penghapusan logis (Soft Delete).