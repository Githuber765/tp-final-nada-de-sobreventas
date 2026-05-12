from sqlalchemy import Column, Integer, String
from payments.database.connection import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
