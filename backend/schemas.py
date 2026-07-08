from pydantic import BaseModel, EmailStr

class TenantRegisterRequest(BaseModel):
    company_name: str
    admin_name: str
    email: str     # Kita pakai str biasa dulu agar tidak perlu install email-validator tambahan
    password: str

class TenantRegisterResponse(BaseModel):
    status: str
    message: str
    tenant_id: str
    user_id: str

class TenantLoginRequest(BaseModel):
    email: str
    password: str

class TenantLoginResponse(BaseModel):
    status: str
    message: str
    tenant_id: str
    company_name: str
    role: str
    access_token: str
    token_type: str = "bearer"

class UserCreateRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str

class IngredientCreateRequest(BaseModel):
    sku: str        # Contoh: "BGR-001"
    name: str       # Contoh: "Daging Sapi Patty"
    category: str
    current_stock: float = 0.0
    safety_stock: float = 10.0
    unit_of_measure: str
    purchase_unit: str | None = None
    conversion_multiplier: float | None = 1.0
    expiry_date: str | None = None

class IngredientResponse(BaseModel):
    id: str
    tenant_id: str
    sku: str
    name: str
    category: str
    current_stock: float = 0.0
    safety_stock: float = 0.0
    unit_of_measure: str
    purchase_unit: str | None = None
    conversion_multiplier: float | None = 1.0
    expiry_date: str | None = None

class IngredientUpdateRequest(BaseModel):
    name: str
    category: str
    current_stock: float
    safety_stock: float
    unit_of_measure: str
    purchase_unit: str | None = None
    conversion_multiplier: float | None = 1.0
    expiry_date: str | None = None

class DashboardMetricItem(BaseModel):
    sku: str
    name: str
    current_stock: float
    safety_stock: float
    unit_of_measure: str
    daily_consumption: float
    days_until_stockout: int

class DashboardMetricsResponse(BaseModel):
    total_ingredients: int
    low_stock_items: int
    healthy_stock_items: int
    stockout_predictions: list[DashboardMetricItem]

class PurchaseOrderItemResponse(BaseModel):
    id: str
    ingredient_id: str
    ingredient_name: str
    ingredient_sku: str
    quantity: float
    unit_of_measure: str

class PurchaseOrderResponse(BaseModel):
    id: str
    tenant_id: str
    po_number: str
    supplier_name: str
    status: str
    created_at: str
    items: list[PurchaseOrderItemResponse]

class AuditLogResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    action: str
    entity_type: str
    entity_name: str
    created_at: str
    details: str

class RestockRequest(BaseModel):
    quantity_in_purchase_unit: float

class KitchenExpiryAlertResponse(BaseModel):
    id: str
    sku: str
    name: str
    current_stock: float
    unit_of_measure: str
    expiry_date: str
    days_until_expiry: int
    status: str # "CRITICAL", "WARNING", "SAFE"