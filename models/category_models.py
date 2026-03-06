
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

  
    parent = relationship(
        "Category",
        remote_side=[id],
        back_populates="children"
    )
    children = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete"  
    )
