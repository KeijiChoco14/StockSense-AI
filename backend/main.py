from fastapi import FastAPI, Depends, status, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine
import asyncio
import uuid
import random
from schemas import TenantRegisterRequest, TenantRegisterResponse, TenantLoginRequest, TenantLoginResponse
from schemas import IngredientCreateRequest, IngredientResponse, IngredientUpdateRequest, DashboardMetricsResponse
from schemas import PurchaseOrderResponse, PurchaseOrderItemResponse, AuditLogResponse, RestockRequest, KitchenExpiryAlertResponse
from schemas import UserCreateRequest, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_tenant_id, get_current_user_and_tenant, RequireRole
import json
from datetime import datetime, timedelta
from typing import List

app = FastAPI(title="StockSense AI - API Baseline (SQLite Mode)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Skrip pembuat tabel otomatis saat startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Buat tabel dasar langsung lewat perintah SQL SQLlite
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            company_name TEXT NOT NULL,
            subscription_tier TEXT NOT NULL DEFAULT 'growth',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            email TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff'
        );
        """))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            current_stock REAL DEFAULT 0.0,
            safety_stock REAL DEFAULT 0.0,
            unit_of_measure TEXT NOT NULL,
            purchase_unit TEXT,
            conversion_multiplier REAL DEFAULT 1.0,
            expiry_date TEXT,
            is_deleted INTEGER DEFAULT 0,
            deleted_at TEXT
        );
        """))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            po_number TEXT NOT NULL,
            supplier_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'draft',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS purchase_order_items (
            id TEXT PRIMARY KEY,
            po_id TEXT NOT NULL,
            ingredient_id TEXT NOT NULL,
            quantity REAL NOT NULL
        );
        """))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            old_data TEXT,
            new_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """))

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to StockSense AI SQLite Engine"}

@app.get("/api/v1/healthcheck")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Tes query ke SQLite
        result = await db.execute(text("SELECT 1;"))
        result.scalar()
        return {
            "status": "healthy",
            "database": "connected (SQLite Mode)",
            "file": "stocksense.db"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/api/v1/auth/register", response_model=TenantRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_tenant(payload: TenantRegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Cek apakah email user sudah terdaftar sebelumnya
        email_check = await db.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": payload.email}
        )
        if email_check.scalar() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar di sistem!"
            )

        # 2. Generate ID unik menggunakan UUID
        new_tenant_id = str(uuid.uuid4())
        new_user_id = str(uuid.uuid4())

        # 3. Insert ke tabel tenants
        await db.execute(
            text("""
                INSERT INTO tenants (id, company_name, subscription_tier) 
                VALUES (:id, :company_name, 'growth')
            """),
            {"id": new_tenant_id, "company_name": payload.company_name}
        )

        # 4. Insert ke tabel users
        hashed_password = hash_password(payload.password)
        
        await db.execute(
            text("""
                INSERT INTO users (id, tenant_id, email, hashed_password, full_name, role) 
                VALUES (:id, :tenant_id, :email, :hashed_password, :full_name, 'owner')
            """),
            {
                "id": new_user_id,
                "tenant_id": new_tenant_id,
                "email": payload.email,
                "hashed_password": hashed_password,
                "full_name": payload.admin_name
            }
        )

        # Commit transaksi data ke SQLite
        await db.commit()

        return {
            "status": "success",
            "message": f"Tenant {payload.company_name} dan User Admin berhasil dibuat!",
            "tenant_id": new_tenant_id,
            "user_id": new_user_id
        }

    except HTTPException as http_err:
        await db.rollback()
        raise http_err
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/api/v1/auth/login", response_model=TenantLoginResponse)
async def login_tenant(payload: TenantLoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Cek email dan password
        result = await db.execute(
            text("""
                SELECT u.id, u.tenant_id, u.hashed_password, t.company_name, u.role
                FROM users u
                JOIN tenants t ON u.tenant_id = t.id
                WHERE u.email = :email
            """),
            {"email": payload.email}
        )
        user = result.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Email atau password salah!")

        user_id, tenant_id, stored_password, company_name, role = user

        if not await verify_password(payload.password, stored_password):
            raise HTTPException(status_code=401, detail="Email atau password salah!")

        # Create JWT Token
        access_token = create_access_token(data={"sub": str(user_id), "tenant_id": str(tenant_id), "role": role})

        return {
            "status": "success",
            "message": "Login berhasil!",
            "tenant_id": tenant_id,
            "company_name": company_name,
            "role": role,
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# 1. Endpoint untuk Menambah Bahan Baku Baru
@app.post("/api/v1/ingredients", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    payload: IngredientCreateRequest, 
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(get_current_user_and_tenant)
):
    tenant_id = auth_data["tenant_id"]
    user_id = auth_data["user_id"]
    
    try:
        # Cek apakah SKU sudah dipakai di tenant yang sama
        sku_check = await db.execute(
            text("SELECT id FROM ingredients WHERE tenant_id = :tenant_id AND sku = :sku AND is_deleted = 0"),
            {"tenant_id": tenant_id, "sku": payload.sku}
        )
        if sku_check.scalar() is not None:
            raise HTTPException(
                status_code=400,
                detail="SKU ini sudah terdaftar di restoran Anda!"
            )

        new_ingredient_id = str(uuid.uuid4())
        
        await db.execute(
            text("""
                INSERT INTO ingredients (id, tenant_id, sku, name, category, current_stock, safety_stock, unit_of_measure, purchase_unit, conversion_multiplier, expiry_date)
                VALUES (:id, :tenant_id, :sku, :name, :category, :current_stock, :safety_stock, :unit_of_measure, :purchase_unit, :conversion_multiplier, :expiry_date)
            """),
            {
                "id": new_ingredient_id,
                "tenant_id": tenant_id,
                "sku": payload.sku,
                "name": payload.name,
                "category": payload.category,
                "current_stock": payload.current_stock,
                "safety_stock": payload.safety_stock,
                "unit_of_measure": payload.unit_of_measure,
                "purchase_unit": payload.purchase_unit,
                "conversion_multiplier": payload.conversion_multiplier,
                "expiry_date": payload.expiry_date
            }
        )
        
        # Log Audit
        await db.execute(
            text("""
                INSERT INTO audit_logs (id, tenant_id, user_id, action, entity_type, entity_id, new_data)
                VALUES (:id, :tenant_id, :user_id, 'CREATE', 'INGREDIENT', :entity_id, :new_data)
            """),
            {
                "id": str(uuid.uuid4()),
                "tenant_id": tenant_id,
                "user_id": user_id,
                "entity_id": new_ingredient_id,
                "new_data": json.dumps(payload.model_dump())
            }
        )
        
        await db.commit()

        return {
            "id": new_ingredient_id,
            "tenant_id": tenant_id,
            "sku": payload.sku,
            "name": payload.name,
            "category": payload.category,
            "current_stock": payload.current_stock,
            "safety_stock": payload.safety_stock,
            "unit_of_measure": payload.unit_of_measure,
            "purchase_unit": payload.purchase_unit,
            "conversion_multiplier": payload.conversion_multiplier,
            "expiry_date": payload.expiry_date
        }
    except HTTPException as http_err:
        await db.rollback()
        raise http_err
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# 2. Endpoint untuk Mengambil Daftar Bahan Baku
@app.get("/api/v1/ingredients", response_model=List[IngredientResponse])
async def get_ingredients(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    result = await db.execute(
        text("SELECT id, tenant_id, sku, name, category, current_stock, safety_stock, unit_of_measure, purchase_unit, conversion_multiplier, expiry_date FROM ingredients WHERE tenant_id = :tenant_id AND is_deleted = 0"),
        {"tenant_id": tenant_id}
    )
    
    ingredients = []
    for row in result.fetchall():
        ingredients.append({
            "id": row[0],
            "tenant_id": row[1],
            "sku": row[2],
            "name": row[3],
            "category": row[4],
            "current_stock": row[5],
            "safety_stock": row[6],
            "unit_of_measure": row[7],
            "purchase_unit": row[8],
            "conversion_multiplier": row[9],
            "expiry_date": row[10]
        })
    return ingredients

# 3. Endpoint untuk Mengedit Bahan Baku
@app.put("/api/v1/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: str, 
    payload: IngredientUpdateRequest, 
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(get_current_user_and_tenant)
):
    tenant_id = auth_data["tenant_id"]
    user_id = auth_data["user_id"]
    
    try:
        # Cek apakah bahan baku ada dan belum dihapus
        check = await db.execute(
            text("SELECT id, tenant_id, sku, name, category, current_stock, safety_stock, unit_of_measure, purchase_unit, conversion_multiplier, expiry_date FROM ingredients WHERE id = :id AND tenant_id = :tenant_id AND is_deleted = 0"),
            {"id": ingredient_id, "tenant_id": tenant_id}
        )
        row = check.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")
            
        await db.execute(
            text("""
                UPDATE ingredients 
                SET name = :name, category = :category, current_stock = :current_stock, 
                    safety_stock = :safety_stock, unit_of_measure = :unit_of_measure,
                    purchase_unit = :purchase_unit, conversion_multiplier = :conversion_multiplier,
                    expiry_date = :expiry_date
                WHERE id = :id
            """),
            {
                "id": ingredient_id,
                "name": payload.name,
                "category": payload.category,
                "current_stock": payload.current_stock,
                "safety_stock": payload.safety_stock,
                "unit_of_measure": payload.unit_of_measure,
                "purchase_unit": payload.purchase_unit,
                "conversion_multiplier": payload.conversion_multiplier,
                "expiry_date": payload.expiry_date
            }
        )
        await db.commit()

        return {
            "id": ingredient_id,
            "tenant_id": row[1],
            "sku": row[2],
            **payload.model_dump()
        }
    except HTTPException as http_err:
        await db.rollback()
        raise http_err
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 3b. Endpoint untuk Soft Delete Bahan Baku
@app.delete("/api/v1/ingredients/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: str, 
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(RequireRole(["owner", "admin"]))
):
    tenant_id = auth_data["tenant_id"]
    user_id = auth_data["user_id"]
    
    try:
        check = await db.execute(
            text("SELECT name, sku FROM ingredients WHERE id = :id AND tenant_id = :tenant_id AND is_deleted = 0"),
            {"id": ingredient_id, "tenant_id": tenant_id}
        )
        row = check.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")
            
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        await db.execute(
            text("UPDATE ingredients SET is_deleted = 1, deleted_at = :now WHERE id = :id"),
            {"now": now_str, "id": ingredient_id}
        )
        
        await db.execute(
            text("""
                INSERT INTO audit_logs (id, tenant_id, user_id, action, entity_type, entity_id, old_data)
                VALUES (:log_id, :tenant_id, :user_id, 'DELETE', 'INGREDIENT', :entity_id, :old_data)
            """),
            {
                "log_id": str(uuid.uuid4()),
                "tenant_id": tenant_id,
                "user_id": user_id,
                "entity_id": ingredient_id,
                "old_data": json.dumps({"name": row[0], "sku": row[1]})
            }
        )
        
        await db.commit()
        return {"status": "success", "message": f"Bahan baku {row[0]} berhasil dihapus"}
    except HTTPException as http_err:
        await db.rollback()
        raise http_err
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 3c. Endpoint untuk Restock (Penerimaan Barang) dengan Multi-unit conversion
@app.post("/api/v1/ingredients/{ingredient_id}/restock")
async def restock_ingredient(
    ingredient_id: str,
    payload: RestockRequest,
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(get_current_user_and_tenant)
):
    tenant_id = auth_data["tenant_id"]
    user_id = auth_data["user_id"]
    
    try:
        check = await db.execute(
            text("SELECT name, current_stock, purchase_unit, conversion_multiplier, unit_of_measure FROM ingredients WHERE id = :id AND tenant_id = :tenant_id AND is_deleted = 0"),
            {"id": ingredient_id, "tenant_id": tenant_id}
        )
        row = check.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")
            
        ing_name = row[0]
        current_stock = row[1]
        p_unit = row[2] or "Grosir"
        multiplier = row[3] if row[3] is not None else 1.0
        uom = row[4]
        
        added_stock = payload.quantity_in_purchase_unit * multiplier
        new_stock = current_stock + added_stock
        
        await db.execute(
            text("UPDATE ingredients SET current_stock = :new_stock WHERE id = :id"),
            {"new_stock": new_stock, "id": ingredient_id}
        )
        
        # Log Audit
        await db.execute(
            text("""
                INSERT INTO audit_logs (id, tenant_id, user_id, action, entity_type, entity_id, new_data)
                VALUES (:log_id, :tenant_id, :user_id, 'UPDATE', 'INGREDIENT_RESTOCK', :entity_id, :new_data)
            """),
            {
                "log_id": str(uuid.uuid4()),
                "tenant_id": tenant_id,
                "user_id": user_id,
                "entity_id": ingredient_id,
                "new_data": json.dumps({
                    "name": ing_name,
                    "action": f"Restock {payload.quantity_in_purchase_unit} {p_unit} (+{added_stock} {uom})",
                    "previous_stock": current_stock,
                    "new_stock": new_stock
                })
            }
        )
        
        await db.commit()
        return {
            "status": "success", 
            "message": f"Berhasil menambah {added_stock} {uom} ke {ing_name}",
            "new_stock": new_stock
        }
    except HTTPException as http_err:
        await db.rollback()
        raise http_err
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 4. Endpoint Dashboard Metrics (US-201)
@app.get("/api/v1/dashboard/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    result = await db.execute(
        text("SELECT sku, name, current_stock, safety_stock, unit_of_measure FROM ingredients WHERE tenant_id = :tenant_id AND is_deleted = 0"),
        {"tenant_id": tenant_id}
    )
    
    rows = result.fetchall()
    
    total_ingredients = len(rows)
    low_stock_items = 0
    predictions = []
    
    for row in rows:
        sku, name, current_stock, safety_stock, unit_of_measure = row
        
        if current_stock <= safety_stock:
            low_stock_items += 1
            
        # Simulasi AI: Men-generate mock 'daily_consumption' berdasarkan rata-rata historis bayangan
        # Agar realistis, kita set konsumsi harian sekitar 1% hingga 10% dari safety stock atau current stock
        base_calc = safety_stock if safety_stock > 0 else (current_stock if current_stock > 0 else 10)
        daily_consumption = round(random.uniform(0.01, 0.1) * base_calc, 2)
        if daily_consumption == 0:
            daily_consumption = 0.5 # Default minimum
            
        days_until_stockout = int(current_stock // daily_consumption) if daily_consumption > 0 else 999
        
        predictions.append({
            "sku": sku,
            "name": name,
            "current_stock": current_stock,
            "safety_stock": safety_stock,
            "unit_of_measure": unit_of_measure,
            "daily_consumption": daily_consumption,
            "days_until_stockout": days_until_stockout
        })
        
    # Sort items by most critical (lowest days until stockout)
    predictions.sort(key=lambda x: x["days_until_stockout"])
    
    # Ambil top 5 paling kritis
    critical_predictions = predictions[:5]
    
    return {
        "total_ingredients": total_ingredients,
        "low_stock_items": low_stock_items,
        "healthy_stock_items": total_ingredients - low_stock_items,
        "stockout_predictions": critical_predictions
    }

# 5. Endpoint Auto-Generate PO (US-301)
@app.post("/api/v1/procurement/auto-generate", response_model=List[PurchaseOrderResponse])
async def auto_generate_po(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        # Cari barang yang kritis (current_stock <= safety_stock)
        critical_items = await db.execute(
            text("SELECT id, sku, name, current_stock, safety_stock, unit_of_measure FROM ingredients WHERE tenant_id = :tenant_id AND current_stock <= safety_stock AND is_deleted = 0"),
            {"tenant_id": tenant_id}
        )
        
        rows = critical_items.fetchall()
        
        if not rows:
            return [] # Tidak ada PO yang dibuat
            
        # Untuk MVP, kita gabungkan semua ke 1 supplier dummy "General Supplier (Auto)"
        po_id = str(uuid.uuid4())
        # Generate PO number like PO-20260708-XXXX
        import datetime
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        po_number = f"PO-{date_str}-{str(uuid.uuid4())[:4].upper()}"
        
        await db.execute(
            text("""
                INSERT INTO purchase_orders (id, tenant_id, po_number, supplier_name, status)
                VALUES (:id, :tenant_id, :po_number, 'General Supplier (Auto)', 'draft')
            """),
            {
                "id": po_id,
                "tenant_id": tenant_id,
                "po_number": po_number
            }
        )
        
        items_responses = []
        
        for row in rows:
            ing_id, sku, name, current, safety, uom = row
            
            # AI Logic sederhana: Pesan sebanyak (safety_stock * 2) - current_stock, atau mock aja minimum 10
            base_calc = safety if safety > 0 else 10
            qty_to_order = round((base_calc * 2) - current, 2)
            if qty_to_order <= 0:
                qty_to_order = 10.0
                
            item_id = str(uuid.uuid4())
            await db.execute(
                text("""
                    INSERT INTO purchase_order_items (id, po_id, ingredient_id, quantity)
                    VALUES (:id, :po_id, :ingredient_id, :quantity)
                """),
                {
                    "id": item_id,
                    "po_id": po_id,
                    "ingredient_id": ing_id,
                    "quantity": qty_to_order
                }
            )
            
            items_responses.append({
                "id": item_id,
                "ingredient_id": ing_id,
                "ingredient_name": name,
                "ingredient_sku": sku,
                "quantity": qty_to_order,
                "unit_of_measure": uom
            })
            
        await db.commit()
        
        # Ambil tanggal dari DB atau gunakan sekarang
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return [{
            "id": po_id,
            "tenant_id": tenant_id,
            "po_number": po_number,
            "supplier_name": "General Supplier (Auto)",
            "status": "draft",
            "created_at": now_str,
            "items": items_responses
        }]
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 6. Endpoint Get PO List
@app.get("/api/v1/procurement", response_model=List[PurchaseOrderResponse])
async def get_procurement_list(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        orders_result = await db.execute(
            text("SELECT id, tenant_id, po_number, supplier_name, status, created_at FROM purchase_orders WHERE tenant_id = :tenant_id ORDER BY created_at DESC"),
            {"tenant_id": tenant_id}
        )
        
        orders = orders_result.fetchall()
        response_list = []
        
        for po in orders:
            po_id, t_id, po_number, supplier, status_val, created_at = po
            
            items_result = await db.execute(
                text("""
                    SELECT poi.id, poi.ingredient_id, i.name, i.sku, poi.quantity, i.unit_of_measure
                    FROM purchase_order_items poi
                    JOIN ingredients i ON poi.ingredient_id = i.id
                    WHERE poi.po_id = :po_id
                """),
                {"po_id": po_id}
            )
            
            items = items_result.fetchall()
            item_list = []
            for item in items:
                i_id, ing_id, i_name, i_sku, qty, uom = item
                item_list.append({
                    "id": i_id,
                    "ingredient_id": ing_id,
                    "ingredient_name": i_name,
                    "ingredient_sku": i_sku,
                    "quantity": qty,
                    "unit_of_measure": uom
                })
                
            response_list.append({
                "id": po_id,
                "tenant_id": t_id,
                "po_number": po_number,
                "supplier_name": supplier,
                "status": status_val,
                "created_at": created_at,
                "items": item_list
            })
            
        return response_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Endpoint Kitchen Expiry Alerts (US-401)
@app.get("/api/v1/kitchen/expiry-alerts", response_model=List[KitchenExpiryAlertResponse])
async def get_expiry_alerts(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        from datetime import datetime
        # Hanya ambil bahan baku yang memiliki expiry date (dan belum dihapus)
        result = await db.execute(
            text("""
                SELECT id, sku, name, current_stock, unit_of_measure, expiry_date 
                FROM ingredients 
                WHERE tenant_id = :tenant_id 
                  AND is_deleted = 0 
                  AND expiry_date IS NOT NULL 
                  AND expiry_date != ''
                  AND current_stock > 0
            """),
            {"tenant_id": tenant_id}
        )
        
        alerts = []
        today = datetime.now().date()
        
        for row in result.fetchall():
            exp_date_str = row[5]
            try:
                exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
                delta = (exp_date - today).days
                
                status = "SAFE"
                if delta <= 2:
                    status = "CRITICAL"
                elif delta <= 7:
                    status = "WARNING"
                
                alerts.append({
                    "id": row[0],
                    "sku": row[1],
                    "name": row[2],
                    "current_stock": row[3],
                    "unit_of_measure": row[4],
                    "expiry_date": exp_date_str,
                    "days_until_expiry": delta,
                    "status": status
                })
            except Exception as e:
                # Jika format tanggal salah, skip
                continue
                
        # Sortir agar yang paling kritis (days_until_expiry terkecil) ada di atas
        alerts.sort(key=lambda x: x["days_until_expiry"])
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Endpoint Ekspor CSV Inventory (US-Export)
@app.get("/api/v1/export/inventory")
async def export_inventory_csv(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        result = await db.execute(
            text("SELECT sku, name, category, current_stock, safety_stock, unit_of_measure, expiry_date FROM ingredients WHERE tenant_id = :tenant_id AND is_deleted = 0"),
            {"tenant_id": tenant_id}
        )
        
        csv_data = "SKU,Nama Barang,Kategori,Stok Saat Ini,Safety Stock,Satuan,Kedaluwarsa\n"
        for row in result.fetchall():
            csv_data += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6] or '-'}\n"
            
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=inventory_report.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. Endpoint Ekspor CSV Audit Logs (US-Export)
@app.get("/api/v1/export/audit-logs")
async def export_audit_logs_csv(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        result = await db.execute(
            text("""
                SELECT created_at, action, entity_type, old_data, new_data
                FROM audit_logs
                WHERE tenant_id = :tenant_id
                ORDER BY created_at DESC
            """),
            {"tenant_id": tenant_id}
        )
        
        csv_data = "Tanggal,Aksi,Tipe Data,Data Lama,Data Baru\n"
        for row in result.fetchall():
            # escape quotes for CSV
            old_data = (row[3] or "").replace('"', '""')
            new_data = (row[4] or "").replace('"', '""')
            csv_data += f"{row[0]},{row[1]},{row[2]},\"{old_data}\",\"{new_data}\"\n"
            
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=audit_logs_report.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 11. Endpoint Users (User Management)
@app.get("/api/v1/users", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(RequireRole(["owner", "admin"]))
):
    try:
        tenant_id = auth_data["tenant_id"]
        result = await db.execute(
            text("SELECT id, email, full_name, role FROM users WHERE tenant_id = :tenant_id ORDER BY created_at ASC"),
            {"tenant_id": tenant_id}
        )
        users = []
        for row in result.fetchall():
            users.append({
                "id": row[0],
                "email": row[1],
                "full_name": row[2],
                "role": row[3]
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(
    payload: UserCreateRequest,
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(RequireRole(["owner", "admin"]))
):
    try:
        tenant_id = auth_data["tenant_id"]
        
        # Check if email exists
        email_check = await db.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": payload.email}
        )
        if email_check.scalar() is not None:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar.")
            
        new_user_id = str(uuid.uuid4())
        hashed = hash_password(payload.password)
        
        await db.execute(
            text("""
                INSERT INTO users (id, tenant_id, email, hashed_password, full_name, role)
                VALUES (:id, :tenant_id, :email, :password, :full_name, :role)
            """),
            {
                "id": new_user_id,
                "tenant_id": tenant_id,
                "email": payload.email,
                "password": hashed,
                "full_name": payload.full_name,
                "role": payload.role
            }
        )
        await db.commit()
        
        return {
            "id": new_user_id,
            "email": payload.email,
            "full_name": payload.full_name,
            "role": payload.role
        }
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/users/{target_user_id}")
async def delete_user(
    target_user_id: str,
    db: AsyncSession = Depends(get_db),
    auth_data: dict = Depends(RequireRole(["owner", "admin"]))
):
    try:
        tenant_id = auth_data["tenant_id"]
        current_user_id = auth_data["user_id"]
        
        if current_user_id == target_user_id:
            raise HTTPException(status_code=400, detail="Anda tidak dapat menghapus akun Anda sendiri.")
            
        # Check if user exists in the same tenant
        check = await db.execute(
            text("SELECT role FROM users WHERE id = :id AND tenant_id = :tenant_id"),
            {"id": target_user_id, "tenant_id": tenant_id}
        )
        row = check.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")
            
        if row[0] == "owner":
            raise HTTPException(status_code=400, detail="Akun Owner tidak dapat dihapus.")
            
        await db.execute(
            text("DELETE FROM users WHERE id = :id AND tenant_id = :tenant_id"),
            {"id": target_user_id, "tenant_id": tenant_id}
        )
        await db.commit()
        return {"status": "success", "message": "Pengguna berhasil dihapus."}
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# 8. Endpoint Get Audit Logs (US-102)
@app.get("/api/v1/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        logs_result = await db.execute(
            text("""
                SELECT a.id, a.user_id, u.full_name, a.action, a.entity_type, a.entity_id, a.old_data, a.new_data, a.created_at
                FROM audit_logs a
                JOIN users u ON a.user_id = u.id
                WHERE a.tenant_id = :tenant_id
                ORDER BY a.created_at DESC
                LIMIT 100
            """),
            {"tenant_id": tenant_id}
        )
        
        logs = logs_result.fetchall()
        response_list = []
        
        for log in logs:
            l_id, u_id, u_name, action, e_type, e_id, old_data, new_data, created_at = log
            
            # Extract name from old/new data if possible to show to user
            entity_name = "Unknown Item"
            details = ""
            
            if action == 'CREATE' and new_data:
                try:
                    data = json.loads(new_data)
                    entity_name = f"{data.get('sku', '')} - {data.get('name', '')}"
                    details = f"Dibuat dengan stok awal {data.get('current_stock')}"
                except: pass
            elif action == 'UPDATE' and old_data and new_data:
                try:
                    old_obj = json.loads(old_data)
                    new_obj = json.loads(new_data)
                    entity_name = f"{old_obj.get('name', 'Item')}"
                    
                    changes = []
                    for k in ['name', 'current_stock', 'safety_stock', 'unit_of_measure']:
                        if str(old_obj.get(k)) != str(new_obj.get(k)):
                            changes.append(f"{k} ({old_obj.get(k)} ➔ {new_obj.get(k)})")
                    details = "Perubahan: " + ", ".join(changes) if changes else "Tidak ada perubahan spesifik"
                except: pass
            elif action == 'DELETE' and old_data:
                try:
                    old_obj = json.loads(old_data)
                    entity_name = f"{old_obj.get('sku', '')} - {old_obj.get('name', '')}"
                    details = "Data dihapus"
                except: pass
            elif e_type == 'INGREDIENT_RESTOCK' and new_data:
                try:
                    new_obj = json.loads(new_data)
                    entity_name = new_obj.get('name', 'Bahan Baku (Restock)')
                    details = new_obj.get('action', 'Penerimaan barang')
                except: pass
                
            response_list.append({
                "id": l_id,
                "user_id": u_id,
                "user_name": u_name,
                "action": action,
                "entity_type": e_type,
                "entity_name": entity_name,
                "created_at": created_at,
                "details": details
            })
            
        return response_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))