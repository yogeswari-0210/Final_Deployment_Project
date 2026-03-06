from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from database.database import Base
from datetime import datetime

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    code = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
