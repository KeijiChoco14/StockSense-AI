# 13. API Specification & Response Wrappers

Seluruh komunikasi antara Frontend (Next.js 15) dan Backend (FastAPI) wajib mematuhi standar RESTful API dengan format payload JSON dan skema respons yang seragam.

---

## 1. Format Respons Seragam (Standard Response Wrapper)

Setiap respons HTTP yang dikembalikan oleh server wajib dibungkus dengan struktur standar berikut untuk mempermudah parsing data di sisi klien:

### Respons Sukses (Standard Success Wrapper)
{
  "success": true,
  "message": "Resource retrieved successfully",
  "data": {} 
}

### Respons Gagal/Error (Standard Error Wrapper)
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "sku",
      "detail": "SKU code must be alphanumeric and upper case"
    }
  ]
}

---

## 2. Endpoint Core: Manajemen Inventaris

### GET /api/v1/ingredients
- Deskripsi: Mengambil daftar semua bahan baku inventaris milik tenant aktif yang tidak dihapus (Soft Delete).
- Headers: Authorization: Bearer <JWT_TOKEN>
- Query Parameters:
  - page (int, default: 1)
  - size (int, default: 20)
  - category (string, optional)
- Respons Sukses (200 OK):
{
  "success": true,
  "message": "Ingredients fetched successfully",
  "data": {
    "items": [
      {
        "id": "a3b8c9d0-1234-5678-90ab-cdef12345678",
        "sku": "RAW-MILK-01",
        "name": "Susu Segar 1L",
        "category": "Dairy",
        "current_stock": 25.5000,
        "safety_stock": 10.0000,
        "unit_of_measure": "liter",
        "status": "SAFE"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 20
  }
}

### POST /api/v1/ingredients
- Deskripsi: Menambahkan SKU bahan baku baru ke dalam database tenant.
- Headers: Authorization: Bearer <JWT_TOKEN>
- Request Body:
{
  "sku": "RAW-MILK-01",
  "name": "Susu Segar 1L",
  "category": "Dairy",
  "safety_stock": 10.0000,
  "unit_of_measure": "liter"
}
- Respons Sukses (201 Created):
{
  "success": true,
  "message": "Ingredient created successfully",
  "data": {
    "id": "a3b8c9d0-1234-5678-90ab-cdef12345678",
    "sku": "RAW-MILK-01"
  }
}