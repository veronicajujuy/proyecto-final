from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from src.db.database import Base


class City(Base):
    """
    Modelo ORM que representa la tabla 'cities' en la base de datos.
    Esta clase define la estructura y las relaciones de la entidad 'City',
    permitiendo mapear filas de la tabla 'cities' a objetos Python mediante SQLAlchemy.
    
    Atributos:
        CityID (int): Identificador único de la ciudad (clave primaria).
        CityName (str): Nombre de la ciudad.
        CountryID (int): Identificador del país al que pertenece la ciudad (clave foránea).

    Relaciones:
        country (Country): Relación con el modelo Country, representando el país de la ciudad.
        employees (List[Employee]): Relación uno-a-muchos con los empleados asociados a la ciudad.
        customers (List[Customer]): Relación uno-a-muchos con los clientes asociados a la ciudad.

    Ejemplo de uso:
        >>> nueva_ciudad = City(CityName="Buenos Aires", CountryID=1)
        >>> session.add(nueva_ciudad)
        >>> session.commit()
    """
    __tablename__ = "cities"

    CityID = Column(Integer, primary_key=True)
    CityName = Column(String(45))
    CountryID = Column(DECIMAL(5, 0))
    CountryID = Column(Integer, ForeignKey("countries.CountryID"))

    country = relationship("Country", back_populates="cities")
    employees = relationship("Employee", back_populates="city")
    customers = relationship("Customer", back_populates="city")
