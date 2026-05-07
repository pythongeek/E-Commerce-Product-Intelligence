from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import uuid

from app.core.database import get_db
from app.core.config import get_settings
from app.models.models import Product, AnalysisJob
from app.tasks.product_analysis import analyze_product_task
from app.api.auth import AuthService

router = APIRouter()
settings = get_settings()

class AnalyzeRequest(BaseModel):
    product_name: str
    product_url: Optional[str] = None
    target_market: str = "US"
    selling_platform: str = "amazon"
    options: dict = {}

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress_pct: int
    current_step: Optional[str]
    product_id: Optional[str]
    error_message: Optional[str]
    created_at: Optional[str]
    completed_at: Optional[str]

@router.post("/analyze")
async def analyze_product(
    data: AnalyzeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # For demo purposes, using a fixed tenant_id
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    # Create job record
    job = AnalysisJob(
        tenant_id=tenant_id,
        status="queued",
        current_step="starting",
        progress_pct=0,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Queue Celery task
    analyze_product_task.delay(
        job_id=str(job.id),
        tenant_id=str(tenant_id),
        product_name=data.product_name,
        target_market=data.target_market,
        selling_platform=data.selling_platform,
    )
    
    return {
        "job_id": str(job.id),
        "status": "queued",
        "message": "Analysis started. Poll /products/analyze/{job_id} for status.",
    }

@router.get("/analyze/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    result = await db.execute(select(AnalysisJob).where(AnalysisJob.id == job_uuid))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
        job_id=str(job.id),
        status=job.status,
        progress_pct=job.progress_pct,
        current_step=job.current_step,
        product_id=str(job.product_id) if job.product_id else None,
        error_message=job.error_message,
        created_at=job.created_at.isoformat() if job.created_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
    )

@router.get("/{product_id}")
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    try:
        prod_uuid = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    result = await db.execute(select(Product).where(Product.id == prod_uuid))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "product_id": str(product.id),
        "product_name": product.product_name,
        "target_market": product.target_market,
        "verdict": product.verdict,
        "product_score": product.product_score,
        "confidence_score": product.confidence_score,
        "score_breakdown": product.score_breakdown,
        "ai_analysis": product.ai_analysis_full,
        "raw_signals": {
            "facebook_ads": product.facebook_ads_data,
            "alibaba": product.alibaba_data,
            "amazon": product.amazon_data,
            "google_trends": product.google_trends_data,
        },
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }

@router.get("/")
async def list_products(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    result = await db.execute(
        select(Product)
        .where(Product.tenant_id == tenant_id)
        .order_by(Product.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    products = result.scalars().all()
    
    return {
        "items": [
            {
                "product_id": str(p.id),
                "product_name": p.product_name,
                "verdict": p.verdict,
                "product_score": p.product_score,
                "confidence_score": p.confidence_score,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in products
        ],
        "total": len(products),
        "limit": limit,
        "offset": offset,
    }
