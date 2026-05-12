from sqlalchemy import Column, Integer, String, Float
from catalog.database.connection import Base

class Product(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
