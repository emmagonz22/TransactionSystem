from sqlalchemy import Column, Integer, String
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

    devices = relationship("Device", backref="people", cascade="all, delete")
