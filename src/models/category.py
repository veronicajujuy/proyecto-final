from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class Category(Base):
    """
    Modelo ORM que representa la tabla 'categories' en la base de datos.

    Esta clase define la estructura y las relaciones de la entidad 'Category', 
    permitiendo mapear filas de la tabla 'categories' a objetos Python mediante SQLAlchemy.

    Atributos:
        CategoryID (int): Identificador único de la categoría (clave primaria).
        CategoryName (str): Nombre de la categoría.
        products (List[Product]): Relación uno-a-muchos con los productos asociados a la categoría.

    Ejemplo de uso:
        >>> nueva_categoria = Category(CategoryName="Bebidas")
        >>> session.add(nueva_categoria)
        >>> session.commit()
    """
    
    __tablename__ = "categories"

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(45))

    products = relationship("Product", back_populates="category")
