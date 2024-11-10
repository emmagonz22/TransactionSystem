from sqlalchemy import Column, Integer, String, Boolean
from db import Base

class Promotion(Base):
    __tablename__ = "promotion"

    pid = Column(Integer, primary_key=True)
    client_email = Column(String(255), nullable=False)
    telephone = Column(String(20))
    promotion = Column(String(255))
    responded = Column(Boolean, default=False)
