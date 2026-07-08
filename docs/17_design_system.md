# 17. Design System Tokens & Component Library

Implementasi token visual dan pustaka komponen antarmuka StockSense AI dibangun di atas fondasi Tailwind CSS, komponen shadcn/ui, serta validasi skema form yang ketat menggunakan Zod.

---

## 1. Token Warna (Color Tokens)

Kami menggunakan palet warna netral berbasis slate yang berpadu dengan aksen status fungsional yang tegas:

// Theme Color Configuration Overview
- background: "#09090b" // Slate Tergelap (Zinc 950)
- foreground: "#fafafa" // Putih Murni (Zinc 50)
- border: "#27272a"     // Abu Tepi Halus (Zinc 800)
- brand.DEFAULT: "#3b82f6" // Blue Neon
- status.safe: "#10b981"   // Emerald (Aman)
- status.warning: "#f59e0b" // Amber (Peringatan)
- status.critical: "#ef4444" // Red (Kritis / Habis)

---

## 2. Validasi Form & Komponen Klien (Zod Integration)

Setiap komponen form masukan data di frontend Next.js wajib divalidasi di sisi klien menggunakan pustaka Zod sebelum payload dikirimkan ke endpoint API Backend.

### Contoh Implementasi Skema Validasi Form Bahan Baku (IngredientForm):
- sku: Minimal 3 karakter, maksimal 50 karakter. Hanya boleh berisi huruf kapital, angka, tanda minus, dan underscore.
- name: Minimal 2 karakter, maksimal 255 karakter.
- safety_stock: Bertipe angka dan tidak boleh bernilai negatif (non-negative).