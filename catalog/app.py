from fastapi import FastAPI
from catalog.api.products import router as products_router
from catalog.api.reserve import router as reserve_router
from catalog.database.init import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(products_router)
app.include_router(reserve_router)