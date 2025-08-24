from sqlalchemy import Column, Integer, Enum, Boolean, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from enums import Size, Color


class ProductItem(Base):
    __tablename__ = 'productitems'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    availibility = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    color = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    photo_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)

    product = relationship("Product", back_populates="productitems")
