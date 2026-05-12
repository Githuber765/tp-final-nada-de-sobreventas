import pytest
from unittest.mock import AsyncMock, MagicMock
from payments.services.payment_service import PaymentService
from payments.models.payment import Payment

@pytest.mark.asyncio
async def test_create_payment_intent():
    # Setup mock session
    mock_session = AsyncMock()
    service = PaymentService(mock_session)
    
    # Run test
    payment = await service.create_payment_intent(order_id=1, amount=100.0)
    
    # Assertions
    assert payment.order_id == 1
    assert payment.amount == 100.0
    assert payment.status == "PENDING"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_get_payment_status():
    # Setup mock session
    mock_session = AsyncMock()
    mock_payment = Payment(id=1, order_id=1, amount=100.0, status="COMPLETED")
    
    # Mock execute to return the payment
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_payment
    mock_session.execute.return_value = mock_result
    
    service = PaymentService(mock_session)
    
    # Run test
    payment = await service.get_payment_status(order_id=1)
    
    # Assertions
    assert payment.status == "COMPLETED"
    mock_session.execute.assert_called_once()
