from fastapi import FastAPI
from catalog.api.products import router as products_router
from catalog.api.reserve import router as reserve_router
from catalog.database.init import init_db 
from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()  

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    ) 

app.include_router(products_router)
app.include_router(reserve_router) 
