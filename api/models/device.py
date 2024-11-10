from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Device(Base):
    __tablename__ = "device"

    did = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey("people.pid", ondelete="CASCADE"), nullable=False)
    device_type = Column(String(50), nullable=False)