from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.models.models import User, Tenant, Product, AnalysisJob

router = APIRouter()

@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": [{"id": str(u.id), "email": u.email, "name": u.full_name, "plan": u.tenant.plan if hasattr(u, 'tenant') else "starter"} for u in users]}

@router.get("/metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)):
    # Product counts by verdict
    verdict_result = await db.execute(
        select(Product.verdict, func.count(Product.id))
        .group_by(Product.verdict)
    )
    verdict_counts = {v: c for v, c in verdict_result.all()}
    
    # Total analyses
    total_analyses = await db.execute(select(func.count(Product.id)))
    total = total_analyses.scalar()
    
    # Active jobs
    active_jobs = await db.execute(
        select(func.count(AnalysisJob.id))
        .where(AnalysisJob.status == "processing")
    )
    active = active_jobs.scalar()
    
    return {
        "total_analyses": total,
        "active_jobs": active,
        "verdict_distribution": verdict_counts,
        "system_status": "healthy",
    }

@router.post("/tokens/fb")
async def add_fb_token(token: str, db: AsyncSession = Depends(get_db)):
    # In production, add to Redis token pool
    return {"message": "Token added to pool", "token_preview": token[:10] + "..."}
