from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from payments.models.payment import Payment
from payments.models.transaction import Transaction

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment_intent(self, order_id: int, amount: float) -> Payment:
        payment = Payment(
            order_id=order_id,
            amount=amount,
            status="PENDING",
            created_at=datetime.utcnow()
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_payment_status(self, order_id: int) -> Payment:
        # Query payment status
        result = await self.db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        payment = result.scalars().first()
        if not payment:
            raise Exception("Payment not found")
        return payment
