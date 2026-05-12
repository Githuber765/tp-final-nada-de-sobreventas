from sqlalchemy.ext.asyncio import AsyncSession
from orders.models.order import Order, OrderItem
from payments.services.payment_service import PaymentService
from events.publisher import EventPublisher
from typing import List

class OrderService:
    def __init__(self, db: AsyncSession, publisher: EventPublisher):
        self.db = db
        self.publisher = publisher

    async def create_order(self, items: List[dict]):
        total = sum(item['price'] * item['quantity'] for item in items)
        
        new_order = Order(total=total, status="PENDING")
        self.db.add(new_order)
        await self.db.flush() # Get the order ID without committing
        
        # Payment integration
        service = PaymentService(self.db)
        payment = await service.create_payment_intent(new_order.id, total)
        
        if not payment:
            raise Exception("Payment failed")
        
        for item in items:
            new_item = OrderItem(order_id=new_order.id, **item)
            self.db.add(new_item)
        
        # Publish Event
        self.publisher.publish("OrderPlaced", {
            "order_id": new_order.id,
            "user_id": "user1", # Placeholder
            "amount": float(total)
        })

        await self.db.commit()
        await self.db.refresh(new_order)
        
        return new_order
