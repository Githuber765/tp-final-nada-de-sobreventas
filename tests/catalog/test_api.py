import pytest
from httpx import AsyncClient
from catalog.models.product import Product

@pytest.mark.asyncio
async def test_get_products(client, db_session):
    # Setup - add products
    db_session.add_all([
        Product(nombre="Prod1", precio=10.0, stock=5),
        Product(nombre="Prod2", precio=20.0, stock=10),
    ])
    await db_session.commit()
    
    response = await client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["nombre"] == "Prod1"

@pytest.mark.asyncio
async def test_get_product_detail(client, db_session):
    # Setup - add product
    prod = Product(nombre="Prod3", precio=30.0, stock=15)
    db_session.add(prod)
    await db_session.commit()
    await db_session.refresh(prod)
    
    response = await client.get(f"/products/{prod.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == prod.id
    assert data["nombre"] == "Prod3"

@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get("/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"
