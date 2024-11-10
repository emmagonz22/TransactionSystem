from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class Transaction(Base):
    __tablename__ = "transaction"

    eid = Column(Integer, primary_key=True)
    tid = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    price_per_item = Column(Numeric(10, 2))
    quantity = Column(Integer, nullable=False)
    phone = Column(String(20))
    store = Column(String(100))
