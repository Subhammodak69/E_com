from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)

    # One-to-many relationship
    subcategories = relationship("SubCategory", back_populates="category", cascade="all, delete")
