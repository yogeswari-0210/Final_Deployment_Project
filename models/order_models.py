


from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Float, nullable=False)
    address = Column(String, nullable=True)  # Added address
    payment_method = Column(String, nullable=True)  # Added payment method
    status = Column(String, default="Ordered") # Dynamic status
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
     
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin = relationship("User", foreign_keys=[admin_id])
     
