from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from catalog.database.connection import get_db
from catalog.models.product import Product

router = APIRouter()

@router.get("/products")
async def listar_productos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    productos = result.scalars().all()

    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock
        }
        for p in productos
    ]

@router.get("/products/{product_id}")
async def obtener_producto(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    producto = result.scalar_one_or_none()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock
    }
