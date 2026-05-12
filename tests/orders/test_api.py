import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_order(client):
    # Depending on how FastAPI handles route conflicts, this might hit the wrong endpoint.
    # We will see.
    payload = {
        "items": [
            {"product_id": 1, "quantity": 2, "price": 10.0}
        ]
    }
    response = await client.post("/orders", json=payload)
    # The main.py endpoint expects different payload format:
    # {"producto_id": 1, "cantidad": 2}
    # If it hits main.py endpoint, it might fail or behave unexpectedly.
    
    # If it hits orders/api/orders.py:
    # It expects OrderCreate (items list of OrderItemCreate)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["total"] == 20.0
    assert data["status"] == "PENDING"

@pytest.mark.asyncio
async def test_get_order(client, db_session):
    from orders.models.order import Order
    new_order = Order(total=100.0, status="PENDING")
    db_session.add(new_order)
    await db_session.commit()
    await db_session.refresh(new_order)
    
    response = await client.get(f"/orders/{new_order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == new_order.id
    assert data["total"] == 100.0
    assert data["status"] == "PENDING"

@pytest.mark.asyncio
async def test_get_order_not_found(client):
    response = await client.get("/orders/999")
    assert response.status_code == 404
