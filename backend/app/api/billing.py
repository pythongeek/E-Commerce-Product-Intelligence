from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.core.config import get_settings
from app.models.models import Tenant

router = APIRouter()
settings = get_settings()

@router.get("/plans")
async def list_plans():
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price": 49,
                "currency": "USD",
                "period": "month",
                "features": ["50 analyses/day", "10 watchlist items", "5 exports/month", "Email support"],
                "limits": settings.PLAN_LIMITS["starter"],
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 149,
                "currency": "USD",
                "period": "month",
                "features": ["500 analyses/day", "100 watchlist items", "50 exports/month", "Priority support", "API access"],
                "limits": settings.PLAN_LIMITS["pro"],
            },
            {
                "id": "agency",
                "name": "Agency",
                "price": 499,
                "currency": "USD",
                "period": "month",
                "features": ["5000 analyses/day", "1000 watchlist items", "500 exports/month", "White-label reports", "Dedicated support"],
                "limits": settings.PLAN_LIMITS["agency"],
            },
        ]
    }

@router.get("/usage")
async def get_usage(db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    plan_limits = settings.PLAN_LIMITS.get(tenant.plan, settings.PLAN_LIMITS["starter"])
    
    return {
        "plan": tenant.plan,
        "subscription_status": tenant.subscription_status,
        "daily_analyses_used": tenant.daily_analyses_used,
        "daily_analyses_limit": plan_limits["daily_analyses"],
        "watchlist_limit": plan_limits["watchlist_items"],
        "exports_limit": plan_limits["exports"],
        "reset_at": tenant.daily_reset_at.isoformat() if tenant.daily_reset_at else None,
    }
