from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(String(45))
    MiddleInitial = Column(String(1))
    LastName = Column(String(45))
    CityID = Column(Integer, ForeignKey("cities.CityID"))
    Address = Column(String(90))

    city = relationship("City", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")
