import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from config import settings

security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

import asyncio

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi kecocokan password secara asynchronous agar tidak memblokir event loop."""
    try:
        return await asyncio.to_thread(
            bcrypt.checkpw,
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(data: dict) -> str:
    """Generate JWT Token berdasarkan data payload."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_tenant_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Middleware/Dependency untuk memverifikasi JWT dari Header Authorization.
    Mengembalikan tenant_id yang sah.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tenant_id: str = payload.get("tenant_id")
        if tenant_id is None:
            raise credentials_exception
        return tenant_id
    except jwt.PyJWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception

def get_current_user_and_tenant(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tenant_id: str = payload.get("tenant_id")
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "staff") # default fallback
        if tenant_id is None or user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "tenant_id": tenant_id, "role": role}
    except jwt.PyJWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception

class RequireRole:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_info: dict = Depends(get_current_user_and_tenant)):
        if user_info["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak memiliki izin (role) untuk melakukan aksi ini."
            )
        return user_info
