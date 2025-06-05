from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from src.db.database import Base


class Employee(Base):
    """
    Modelo ORM que representa la tabla 'employees' en la base de datos.
    Esta clase define la estructura y las relaciones de la entidad 'Employee',
    permitiendo mapear filas de la tabla 'employees' a objetos Python mediante SQLAlchemy.

    Atributos:
        EmployeeID (int): Identificador único del empleado (clave primaria).
        FirstName (str): Nombre del empleado.
        MiddleInitial (str): Inicial del segundo nombre del empleado.
        LastName (str): Apellido del empleado.
        BirthDate (date): Fecha de nacimiento del empleado.
        Gender (str): Género del empleado.
        CityID (int): Identificador de la ciudad donde reside el empleado (clave foránea).
        HireDate (datetime): Fecha de contratación del empleado.
    Relaciones:
        city (City): Relación con el modelo City, representando la ciudad del empleado.
        sales (List[Sale]): Relación uno-a-muchos con las ventas asociadas al empleado.
    Ejemplo de uso:
        >>> nuevo_empleado = Employee(FirstName="Ana", MiddleInitial="B", LastName="Gómez", BirthDate="1990-01-01",
        ...     Gender="F", CityID=1, HireDate="2020-01-01 09:00:00")
        >>> session.add(nuevo_empleado)
        >>> session.commit()
    """

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
