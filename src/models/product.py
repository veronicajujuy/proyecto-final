from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from src.db.database import Base


class Product(Base):
    """
    Modelo ORM que representa la tabla 'products' en la base de datos.
    Esta clase define la estructura y las relaciones de la entidad 'Product',
    permitiendo mapear filas de la tabla 'products' a objetos Python mediante SQLAlchemy.
    Atributos:
        ProductID (int): Identificador único del producto (clave primaria).
        ProductName (str): Nombre del producto.
        Price (Decimal): Precio del producto.
        CategoryID (int): Identificador de la categoría a la que pertenece el producto (clave foránea).
        Class (str): Clase del producto.
        ModifyDate (Time): Fecha y hora de la última modificación del producto.
        Resistant (str): Indica si el producto es resistente.
        IsAllergic (str): Indica si el producto es alérgico.
        VitalityDays (Decimal): Días de vitalidad del producto.
    Relaciones:
        category (Category): Relación con el modelo Category, representando la categoría del producto.
        sales (List[Sale]): Relación uno-a-muchos con las ventas asociadas al producto.
    Ejemplo de uso:
        >>> nuevo_producto = Product(ProductName="Agua Mineral", Price=1.50, CategoryID=1, Class="Beverage", ModifyDate="2023-10-01 12:00:00", Resistant="Yes", IsAllergic="No", VitalityDays=30)
        >>> session.add(nuevo_producto)
        >>> session.commit()
    """

    __tablename__ = "products"

    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(45))
    Price = Column(DECIMAL(10, 4))
    CategoryID = Column(Integer, ForeignKey("categories.CategoryID"))
    Class = Column(String(45))
    ModifyDate = Column(Time)
    Resistant = Column(String(45))
    IsAllergic = Column(String(10))
    VitalityDays = Column(DECIMAL(3, 0))

    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
