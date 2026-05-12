from catalog.database.connection import engine, AsyncSessionLocal, Base
from catalog.models.product import Product
from sqlalchemy import select

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        productos = result.scalars().all()
        
        if not productos:
            session.add_all([
                Product(nombre="iPhone 15", precio=1200.0, stock=5),
                Product(nombre="Notebook Gamer", precio=2500.0, stock=3),
                Product(nombre="Auriculares", precio=150.0, stock=10),
            ])
            await session.commit()
