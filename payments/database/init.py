from payments.database.connection import engine, Base
from payments.models.payment import Payment
from payments.models.payment_method import PaymentMethod
from payments.models.transaction import Transaction

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
