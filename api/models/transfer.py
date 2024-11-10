from sqlalchemy import Column, Integer, Numeric, Date
from db import Base

class Transfer(Base):
    __tablename__ = "transfer"
    trid = Column(Integer, primary_key=True)
    sender_id =  Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date)
