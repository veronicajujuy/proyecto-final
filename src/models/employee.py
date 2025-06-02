from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from src.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    EmployeeID = Column(Integer, primary_key=True)
    FirstName = Column(String(45))
    MiddleInitial = Column(String(1))
    LastName = Column(String(45))
    BirthDate = Column(Date)
    Gender = Column(String(1))
    CityID = Column(Integer, ForeignKey("cities.CityID"))
    HireDate = Column(DateTime)

    city = relationship("City", back_populates="employees")
    sales = relationship("Sale", back_populates="employee")
