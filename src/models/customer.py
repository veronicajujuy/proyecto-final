from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base


class Customer(Base):
    """
    Modelo ORM que representa la tabla 'customers' en la base de datos.
    Esta clase define la estructura y las relaciones de la entidad 'Customer',
    permitiendo mapear filas de la tabla 'customers' a objetos Python mediante SQLAlchemy.

    Atributos:
        CustomerID (int): Identificador único del cliente (clave primaria).
        FirstName (str): Nombre del cliente.
        MiddleInitial (str): Inicial del segundo nombre del cliente.
        LastName (str): Apellido del cliente.
        CityID (int): Identificador de la ciudad donde reside el cliente (clave foránea).
        Address (str): Dirección del cliente.
        
    Relaciones:
        city (City): Relación con el modelo City, representando la ciudad del cliente.
        sales (List[Sale]): Relación uno-a-muchos con las ventas asociadas al cliente.

    Ejemplo de uso:
        >>> nuevo_cliente = Customer(FirstName="Juan", MiddleInitial="A", LastName="Pérez", CityID=1, Address="Calle Falsa 123")
        >>> session.add(nuevo_cliente)
        >>> session.commit()
    """

    __tablename__ = "customers"

    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(String(45))
    MiddleInitial = Column(String(1))
    LastName = Column(String(45))
    CityID = Column(Integer, ForeignKey("cities.CityID"))
    Address = Column(String(90))

    city = relationship("City", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")
