from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class Country(Base):
    __tablename__ = "countries"

    CountryID = Column(Integer, primary_key=True)
    CountryName = Column(String(45))
    CountryCode = Column(String(2))

    cities = relationship("City", back_populates="country")
