from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(45))

    products = relationship("Product", back_populates="category")
