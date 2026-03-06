from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OfferBase(BaseModel):
    title: str
    description: str
    discount_percentage: int
    start_date: Optional[datetime] = None
    end_date: datetime
    active: Optional[bool] = True
    code: Optional[str] = None
    image_url: Optional[str] = None

class OfferCreate(OfferBase):
    pass

class OfferRead(OfferBase):
    id: int

    class Config:
        from_attributes = True
