import pytest
from sqlalchemy import select
from payments.models.payment import Payment

@pytest.mark.asyncio
async def test_save_and_retrieve_payment(db_session):
    # Create a payment
    payment = Payment(order_id=1, amount=100.0, status="PENDING")
    db_session.add(payment)
    await db_session.commit()
    await db_session.refresh(payment)
    
    # Retrieve the payment
    result = await db_session.execute(select(Payment).where(Payment.order_id == 1))
    retrieved_payment = result.scalar_one()
    
    # Assertions
    assert retrieved_payment.order_id == 1
    assert retrieved_payment.amount == 100.0
    assert retrieved_payment.status == "PENDING"
