-- 1. Aktifkan Ekstensi UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Buat Tabel tenants
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL,
    subscription_tier VARCHAR(50) NOT NULL DEFAULT 'growth',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Buat Tabel users
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
    deleted_at TIMESTAMPTZ
);

-- 4. Buat Tabel ingredients
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
    CONSTRAINT unique_tenant_sku UNIQUE (tenant_id, sku)
);

-- =========================================================================
-- SECURITY MASTERCLASS: IMPLEMENTASI ROW-LEVEL SECURITY (RLS)
-- =========================================================================

-- Aktifkan RLS di tabel yang sensitif terhadap multi-tenancy
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE ingredients ENABLE ROW LEVEL SECURITY;

-- Buat Policy untuk tabel 'users'
-- Hanya izinkan akses jika tenant_id di baris database cocok dengan context session 'app.current_tenant_id'
CREATE POLICY user_tenant_isolation_policy ON users
    AS PERMISSIVE FOR ALL
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);

-- Buat Policy untuk tabel 'ingredients'
CREATE POLICY ingredient_tenant_isolation_policy ON ingredients
    AS PERMISSIVE FOR ALL
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);