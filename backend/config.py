from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://stocksense_admin:supersecretpassword@localhost:5432/stocksense_ai"
    SECRET_KEY: str = "supersecretjsonwebtokenkeyforstocksenseai2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

settings = Settings()