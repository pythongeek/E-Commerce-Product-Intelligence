from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

from app.core.database import get_db
from app.services.auth.auth_service import AuthService
from app.models.models import User, Tenant, RefreshToken

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    plan: str = "starter"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create tenant
    tenant = Tenant(
        name=f"{data.full_name}'s Workspace",
        plan=data.plan,
    )
    db.add(tenant)
    await db.flush()
    
    # Create user
    user = User(
        tenant_id=tenant.id,
        email=data.email,
        password_hash=AuthService.hash_password(data.password),
        full_name=data.full_name,
        is_verified=True,
    )
    db.add(user)
    await db.commit()
    
    # Generate tokens
    access_token = AuthService.create_access_token({"sub": str(user.id), "tenant_id": str(tenant.id), "plan": tenant.plan})
    refresh_token = AuthService.create_refresh_token({"sub": str(user.id)})
    
    # Save refresh token hash
    token_hash = AuthService.hash_api_key(refresh_token)
    rt = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + datetime.timedelta(days=30),
    )
    db.add(rt)
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=900,
    )

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    
    if not user or not AuthService.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account suspended")
    
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    access_token = AuthService.create_access_token({
        "sub": str(user.id),
        "tenant_id": str(user.tenant_id),
        "plan": user.tenant.plan if hasattr(user, 'tenant') else "starter"
    })
    refresh_token = AuthService.create_refresh_token({"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=900,
    )

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = AuthService.verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    new_access = AuthService.create_access_token({
        "sub": str(user.id),
        "tenant_id": str(user.tenant_id),
        "plan": user.tenant.plan if hasattr(user, 'tenant') else "starter"
    })
    
    return {"access_token": new_access, "token_type": "bearer", "expires_in": 900}
