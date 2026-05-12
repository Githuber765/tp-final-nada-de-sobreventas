from fastapi import FastAPI
from catalog.api.products import router
from catalog.database.init import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router)
