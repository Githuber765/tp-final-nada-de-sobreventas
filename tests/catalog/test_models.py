import pytest
from sqlalchemy import select
from catalog.models.product import Product

@pytest.mark.asyncio
async def test_create_product(db_session):
    # Test model creation
    new_product = Product(nombre="Test Product", precio=10.0, stock=100)
    db_session.add(new_product)
    await db_session.commit()
    await db_session.refresh(new_product)
    
    assert new_product.id is not None
    assert new_product.nombre == "Test Product"
    assert new_product.precio == 10.0
    assert new_product.stock == 100

@pytest.mark.asyncio
async def test_get_product(db_session):
    # Setup
    new_product = Product(nombre="Another Product", precio=20.0, stock=50)
    db_session.add(new_product)
    await db_session.commit()
    
    # Test database interaction
    result = await db_session.execute(select(Product).where(Product.nombre == "Another Product"))
    product = result.scalar_one()
    
    assert product.id == new_product.id
    assert product.precio == 20.0
