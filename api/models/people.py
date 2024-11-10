from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db import Base

class People(Base):
    __tablename__ = "people"

    pid = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    telephone = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    android = Column(Boolean, default=False)
    ios = Column(Boolean, default=False)
    desktop = Column(Boolean, default=False)
