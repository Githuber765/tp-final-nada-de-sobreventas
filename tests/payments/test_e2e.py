import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from payments.api.webhook_handler import router as webhook_router
from payments.services.payment_service import PaymentService
from payments.database.connection import get_db

@pytest.mark.asyncio
async def test_payment_flow(db_session):
    # Setup test app
    app = FastAPI()
    app.include_router(webhook_router)
    
    # Override get_db
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # 1. Create payment
    service = PaymentService(db_session)
    order_id = 1
    amount = 100.0
    payment = await service.create_payment_intent(order_id=order_id, amount=amount)
    assert payment.status == "PENDING"
    
    # 2. Webhook call (simulating external provider callback)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhook", json={"order_id": order_id, "status": "COMPLETED"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    # 3. Status verification
    updated_payment = await service.get_payment_status(order_id=order_id)
    assert updated_payment.status == "COMPLETED"

    # Cleanup
    app.dependency_overrides.clear()
