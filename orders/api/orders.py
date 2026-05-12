from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from orders.database.connection import get_db
from orders.models.order import Order, OrderItem
from orders.services.order_service import OrderService
from events.publisher import EventPublisher

router = APIRouter()
publisher = EventPublisher()

# Schemas
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    total: float
    status: str

    class Config:
        from_attributes = True

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    service = OrderService(db, publisher)
    try:
        new_order = await service.create_order([item.model_dump() for item in order_data.items])
        return new_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return order
