from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class Country(Base):
    """Modelo ORM que representa la tabla 'countries' en la base de datos.

    Esta clase define la estructura y las relaciones de la entidad 'Country',
    permitiendo mapear filas de la tabla 'countries' a objetos Python mediante SQLAlchemy.
    Atributos:
        CountryID (int): Identificador único del país (clave primaria).
        CountryName (str): Nombre del país.
        CountryCode (str): Código del país.

    Relaciones:
        cities (List[City]): Relación uno-a-muchos con las ciudades asociadas al país.
    Ejemplo de uso:
        >>> nuevo_pais = Country(CountryName="Argentina", CountryCode="AR")
        >>> session.add(nuevo_pais)
        >>> session.commit()
    """

    __tablename__ = "countries"

    CountryID = Column(Integer, primary_key=True)
    CountryName = Column(String(45))
    CountryCode = Column(String(2))

    cities = relationship("City", back_populates="country")
