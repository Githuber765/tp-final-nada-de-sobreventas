import asyncio
import time

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis

from catalog.database.connection import get_db
from catalog.models.product import Product

router = APIRouter()

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1
)


class ReserveRequest(BaseModel):
    product_id: int
    quantity: int


@router.post("/reserve")
async def reserve_product(request: ReserveRequest, db: AsyncSession = Depends(get_db)):
    if request.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="La cantidad debe ser mayor a 0"
        )

    lock_key = f"lock:product:{request.product_id}"
    lock_value = "reserved"

    lock_acquired = False
    start_time = time.time()

    while time.time() - start_time < 5:
        try:
            lock_acquired = redis_client.set(
                lock_key,
                lock_value,
                nx=True,
                ex=5
            )
        except redis.exceptions.RedisError:
            raise HTTPException(
                status_code=503,
                detail="Redis no disponible. Reintentá más tarde."
            )

        if lock_acquired:
            break

        await asyncio.sleep(0.05)

    if not lock_acquired:
        raise HTTPException(
            status_code=503,
            detail="Otro usuario está reservando este producto. Reintentá."
        )

    try:
        result = await db.execute(
            select(Product).where(Product.id == request.product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        if product.stock < request.quantity:
            raise HTTPException(
                status_code=400,
                detail="Sin stock suficiente"
            )

        product.stock -= request.quantity
        await db.commit()
        await db.refresh(product)

        return {
            "status": "reserved",
            "product_id": product.id,
            "quantity": request.quantity,
            "stock_remaining": product.stock
        }

    finally:
        try:
            redis_client.delete(lock_key)
        except redis.exceptions.RedisError:
            pass