from src.db.database import DBConnection
from src.models import Customer, Category, Product, Employee, Sale
from src.utils.logger import logger


def test_cliente_y_ciudad():
    session = DBConnection().get_session()
    cliente = session.query(Customer).first()
    logger.info(
        f"Cliente: {cliente.FirstName} {cliente.LastName} ciudad: {cliente.city.CityName}"
    )

    assert cliente.city.CityName is not None
    assert cliente.city.CityName != ""
    session.close()


def test_empleados_ciudad_pais():
    session = DBConnection().get_session()
    empleado = session.query(Employee).first()
    logger.info(
        f"Empleado: {empleado.FirstName} {empleado.LastName} ciudad: {empleado.city.CityName} pais: {empleado.city.country.CountryName}"
    )

    assert empleado.city.CityName is not None
    assert empleado.city.CityName != ""
    assert empleado.city.country.CountryName is not None
    assert empleado.city.country.CountryName != ""

def test_categoria_tiene_nombre_y_productos():
    session = DBConnection().get_session()
    categoria = session.query(Category).first()
    if categoria:
        logger.info(
            f"Categoría: {categoria.CategoryName}, Productos: {len(categoria.products) if categoria.products else 0}"
        )
        assert categoria.CategoryName is not None
        assert categoria.CategoryName != ""
        assert hasattr(categoria, "products") # Verifica que la relación exista
        if categoria.products:
            assert isinstance(categoria.products[0], Product)
    session.close()


def test_producto_tiene_categoria():
    session = DBConnection().get_session()
    producto = session.query(Product).first()
    if producto:
        assert producto.category is not None
        assert isinstance(producto.category, Category)


def test_venta_tiene_cliente_producto_empleado():
    session = DBConnection().get_session()
    venta = session.query(Sale).first()
    if venta:
        assert venta.customer is not None
        assert isinstance(venta.customer, Customer)

        assert venta.product is not None
        assert isinstance(venta.product, Product)

        assert venta.employee is not None
        assert isinstance(venta.employee, Employee)

    session.close()
