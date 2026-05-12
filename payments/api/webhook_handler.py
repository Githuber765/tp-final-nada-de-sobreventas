from sqlalchemy import update
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from payments.database.connection import get_db
from payments.models.payment import Payment

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(webhook_data: dict, db: AsyncSession = Depends(get_db)):
    order_id = webhook_data.get("order_id")
    status = webhook_data.get("status")

    if not order_id or not status:
        raise HTTPException(status_code=400, detail="Invalid webhook data")

    # Update payment status in database
    await db.execute(
        update(Payment)
        .where(Payment.order_id == order_id)
        .values(status=status)
    )
    await db.commit()
    
    return {"status": "success"}
