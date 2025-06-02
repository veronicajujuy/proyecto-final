from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from src.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    SalesID = Column(Integer, primary_key=True)
    SalesPersonID = Column(Integer, ForeignKey("employees.EmployeeID"))
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer)
    Discount = Column(DECIMAL(10, 2))
    TotalPrice = Column(DECIMAL(10, 2))
    SalesDate = Column(Time)
    TransactionNumber = Column(String(20))

    employee = relationship("Employee", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    product = relationship("Product", back_populates="sales")
