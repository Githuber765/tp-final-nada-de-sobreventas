from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from payments.database.connection import get_db
from payments.services.payment_service import PaymentService
from pydantic import BaseModel

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    order_id: int
    amount: float

@router.post("/payments/intents")
async def create_payment(request: PaymentIntentRequest, db: AsyncSession = Depends(get_db)):
    service = PaymentService(db)
    try:
        payment = await service.create_payment_intent(request.order_id, request.amount)
        return {"payment_id": payment.id, "status": payment.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payments/{order_id}")
async def get_payment(order_id: int, db: AsyncSession = Depends(get_db)):
    service = PaymentService(db)
    try:
        payment = await service.get_payment_status(order_id)
        return {"payment_id": payment.id, "status": payment.status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
