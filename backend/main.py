from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db

app = FastAPI(title="StockSense AI - API Baseline")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to StockSense AI Backend Engine"}

@app.get("/api/v1/healthcheck")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Tes koneksi ke database Docker
        result = await db.execute(text("SELECT version();"))
        db_version = result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "postgres_version": db_version
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}