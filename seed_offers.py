from sqlalchemy.orm import Session
from database.database import SessionLocal, engine, Base
from models.offer_models import Offer
from datetime import datetime, timedelta

def seed_offers():
    db = SessionLocal()
    
    # Drop and recreate offers table to apply schema changes
    print("Dropping and recreating offers table...")
    Offer.__table__.drop(engine, checkfirst=True)
    Offer.__table__.create(engine)

    offers = [
        {
            "title": "Extra ₹30 OFF",
            "description": "on orders above ₹1250",
            "discount_percentage": 5,
            "start_date": datetime.utcnow() - timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "active": True,
            "code": "SAVE30",
            "image_url": "../assets/belt.png"
        },
        {
            "title": "Extra ₹100 OFF",
            "description": "on orders above ₹3000",
            "discount_percentage": 10,
            "start_date": datetime.utcnow() - timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "active": True,
            "code": "SAVE100",
            "image_url": "../assets/drool_food.png"
        },
        {
            "title": "Expired Offer",
            "description": "This should not appear",
            "discount_percentage": 50,
            "start_date": datetime.utcnow() - timedelta(days=10),
            "end_date": datetime.utcnow() - timedelta(days=1),
            "active": True,
            "code": "EXPIRED",
            "image_url": "../assets/belt.png"
        },
        {
            "title": "Inactive Offer",
            "description": "This should not appear either",
            "discount_percentage": 20,
            "start_date": datetime.utcnow() - timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "active": False,
            "code": "INACTIVE",
            "image_url": "../assets/drool_food.png"
        }
    ]

    for offer_data in offers:
        offer = Offer(**offer_data)
        db.add(offer)
    
    db.commit()
    db.close()
    print("Offers re-seeded successfully with active, inactive, and expired examples.")

if __name__ == "__main__":
    seed_offers()
