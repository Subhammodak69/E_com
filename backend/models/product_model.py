from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base
from models.sub_category_model import SubCategory


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)

    subcategory = relationship("SubCategory", back_populates="products")
