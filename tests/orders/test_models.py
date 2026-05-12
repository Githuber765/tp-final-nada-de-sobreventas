import pytest
import pytest_asyncio
from sqlalchemy.future import select
from orders.models.order import Order, OrderItem
from sqlalchemy.orm import selectinload

@pytest.mark.asyncio
async def test_order_creation(db_session):
    new_order = Order(total=100.0, status="PENDING")
    db_session.add(new_order)
    await db_session.commit()
    await db_session.refresh(new_order)
    
    assert new_order.id is not None
    assert new_order.total == 100.0
    assert new_order.status == "PENDING"

from sqlalchemy.orm import selectinload

@pytest.mark.asyncio
async def test_order_item_creation(db_session):
    new_order = Order(total=100.0, status="PENDING")
    db_session.add(new_order)
    await db_session.commit()
    await db_session.refresh(new_order)
    
    new_item = OrderItem(order_id=new_order.id, product_id=1, quantity=2, price=50.0)
    db_session.add(new_item)
    await db_session.commit()
    await db_session.refresh(new_item)
    
    assert new_item.id is not None
    assert new_item.order_id == new_order.id
    assert new_item.product_id == 1
    assert new_item.quantity == 2
    assert new_item.price == 50.0
    
    # Check relationship using selectinload
    result = await db_session.execute(
        select(Order).options(selectinload(Order.items)).filter(Order.id == new_order.id)
    )
    order = result.scalar_one()
    assert len(order.items) == 1
    assert order.items[0].product_id == 1
