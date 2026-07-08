from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ubah dari PostgreSQL ke SQLite (menggunakan aiosqlite untuk async)
    DATABASE_URL: str = "sqlite+aiosqlite:///./stocksense.db"
    SECRET_KEY: str = "supersecretjsonwebtokenkeyforstocksenseai2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

settings = Settings()