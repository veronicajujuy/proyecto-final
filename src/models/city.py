from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from src.db.database import Base


class City(Base):
    __tablename__ = "cities"

    CityID = Column(Integer, primary_key=True)
    CityName = Column(String(45))
    CountryID = Column(DECIMAL(5, 0))
    CountryID = Column(Integer, ForeignKey("countries.CountryID"))

    country = relationship("Country", back_populates="cities")
    employees = relationship("Employee", back_populates="city")
    customers = relationship("Customer", back_populates="city")
