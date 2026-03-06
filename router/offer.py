from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependency.db_dependency import get_db
from models.offer_models import Offer
from schemas.offer_schemas import OfferRead, OfferCreate
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/offers",
    tags=["offers"]
)

@router.get("/", response_model=List[OfferRead])
def get_offers(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    return db.query(Offer).filter(
        Offer.active == True,
        Offer.start_date <= now,
        Offer.end_date >= now
    ).all()

# Admin endpoint to create offers
@router.post("/admin", response_model=OfferRead)
def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    db_offer = Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

# GET all offers for admin (including inactive/expired)
@router.get("/admin/all", response_model=List[OfferRead])
def get_all_offers_admin(db: Session = Depends(get_db)):
    return db.query(Offer).all()
