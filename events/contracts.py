from pydantic import BaseModel

class OrderCreatedEvent(BaseModel):
    order_id: str
    user_id: str
    amount: float

class PaymentCompletedEvent(BaseModel):
    order_id: str
    payment_id: str
