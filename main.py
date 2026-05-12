from fastapi import FastAPI
from catalog.api.products import router
from orders.api.orders import router as orders_router
from payments.api.payments import router as payments_router
from catalog.database.init import init_db as init_catalog_db
from orders.database.init import init_db as init_orders_db
from payments.database.init import init_db as init_payments_db
from common.observability.middleware import CorrelationIdMiddleware
from common.observability.logging import setup_logging

setup_logging()
app = FastAPI(title="Market-Place-Inc Monolito TP1")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)
app.include_router(orders_router)
app.include_router(payments_router)


@app.on_event("startup")
async def startup():
    await init_catalog_db()
    await init_orders_db()
    await init_payments_db()


@app.get("/health")
async def health():
    return {"status": "ok"}