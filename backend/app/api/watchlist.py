from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.models.models import Watchlist, Product, WatchlistAlert

router = APIRouter()

class WatchlistAddRequest(BaseModel):
    product_id: str
    notify_on_change: bool = True

@router.get("/")
async def get_watchlist(db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    result = await db.execute(
        select(Watchlist, Product)
        .join(Product, Watchlist.product_id == Product.id)
        .where(Watchlist.tenant_id == tenant_id)
        .order_by(Watchlist.added_at.desc())
    )
    items = result.all()
    
    return {
        "items": [
            {
                "watchlist_id": str(w.id),
                "product_id": str(p.id),
                "product_name": p.product_name,
                "verdict": p.verdict,
                "product_score": p.product_score,
                "notify_on_change": w.notify_on_change,
                "added_at": w.added_at.isoformat() if w.added_at else None,
            }
            for w, p in items
        ],
        "total": len(items),
    }

@router.post("/")
async def add_to_watchlist(data: WatchlistAddRequest, db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    try:
        product_uuid = uuid.UUID(data.product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Check if exists
    result = await db.execute(
        select(Watchlist)
        .where(Watchlist.tenant_id == tenant_id)
        .where(Watchlist.product_id == product_uuid)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Product already in watchlist")
    
    watchlist_item = Watchlist(
        tenant_id=tenant_id,
        product_id=product_uuid,
        notify_on_change=data.notify_on_change,
    )
    db.add(watchlist_item)
    await db.commit()
    
    return {"message": "Added to watchlist", "watchlist_id": str(watchlist_item.id)}

@router.delete("/{product_id}")
async def remove_from_watchlist(product_id: str, db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    try:
        product_uuid = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    result = await db.execute(
        select(Watchlist)
        .where(Watchlist.tenant_id == tenant_id)
        .where(Watchlist.product_id == product_uuid)
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Not in watchlist")
    
    await db.delete(item)
    await db.commit()
    
    return {"message": "Removed from watchlist"}

@router.get("/alerts")
async def get_watchlist_alerts(db: AsyncSession = Depends(get_db)):
    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    result = await db.execute(
        select(WatchlistAlert)
        .where(WatchlistAlert.tenant_id == tenant_id)
        .where(WatchlistAlert.is_read == False)
        .order_by(WatchlistAlert.created_at.desc())
    )
    alerts = result.scalars().all()
    
    return {
        "alerts": [
            {
                "alert_id": str(a.id),
                "product_id": str(a.product_id),
                "alert_type": a.alert_type,
                "old_value": a.old_value,
                "new_value": a.new_value,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in alerts
        ],
        "unread_count": len(alerts),
    }
