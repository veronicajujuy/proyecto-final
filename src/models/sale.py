from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from src.db.database import Base


class Sale(Base):
    """
    Modelo ORM que representa la tabla 'sales' en la base de datos.
    Esta clase define la estructura y las relaciones de la entidad 'Sale',
    permitiendo mapear filas de la tabla 'sales' a objetos Python mediante SQLAlchemy.

    Atributos:
        SalesID (int): Identificador único de la venta (clave primaria).
        SalesPersonID (int): Identificador del empleado que realizó la venta (clave foránea).
        CustomerID (int): Identificador del cliente asociado a la venta (clave foránea).
        ProductID (int): Identificador del producto vendido (clave foránea).
        Quantity (int): Cantidad de productos vendidos.
        Discount (Decimal): Descuento aplicado a la venta.
        TotalPrice (Decimal): Precio total de la venta (después de aplicar descuentos).
        SalesDate (Time): Fecha y hora de la venta.
        TransactionNumber (str): Número de transacción de la venta.

    Relaciones:
        employee (Employee): Relación con el modelo Employee, representando al empleado que realizó la venta.
        customer (Customer): Relación con el modelo Customer, representando al cliente asociado a la venta.
        product (Product): Relación con el modelo Product, representando el producto vendido.
    Ejemplo de uso:
        >>> nueva_venta = Sale(SalesPersonID=1, CustomerID=2, ProductID=3, Quantity=5, Discount=10.00, TotalPrice=45.00, SalesDate="2023-10-01 14:30:00", TransactionNumber="TX123456")
        >>> session.add(nueva_venta)
        >>> session.commit()
    """
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
