from sqlalchemy import Column, Integer, String, Float, DateTime
from payments.database.connection import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
