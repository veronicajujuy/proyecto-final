from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from src.db.database import Base


class Product(Base):
    __tablename__ = "products"

    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(45))
    Price = Column(DECIMAL(10, 4))
    CategoryID = Column(Integer, ForeignKey("categories.CategoryID"))
    Class = Column(String(45))
    ModifyDate = Column(Time)
    Resistant = Column(String(45))
    IsAllergic = Column(String(10))
    VitalityDays = Column(DECIMAL(3, 0))

    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
