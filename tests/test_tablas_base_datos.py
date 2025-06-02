from src.db.database import get_session
from src.models import Customer, Category, Product, Employee, Sale
from src.utils.logger import logger


def test_cliente_y_ciudad():
    session = get_session()
    cliente = session.query(Customer).first()
    logger.info(
        f"Cliente: {cliente.FirstName} {cliente.LastName} ciudad: {cliente.city.CityName}"
    )

    assert cliente.city.CityName is not None
    assert cliente.city.CityName != ""


def test_empleados_ciudad_pais():
    session = get_session()
    empleado = session.query(Employee).first()
    logger.info(
        f"Empleado: {empleado.FirstName} {empleado.LastName} ciudad: {empleado.city.CityName} pais: {empleado.city.country.CountryName}"
    )

    assert empleado.city.CityName is not None
    assert empleado.city.CityName != ""
    assert empleado.city.country.CountryName is not None
    assert empleado.city.country.CountryName != ""


def test_producto_tiene_categoria():
    session = get_session()
    producto = session.query(Product).first()
    if producto:
        assert producto.category is not None
        assert isinstance(producto.category, Category)


def test_venta_tiene_cliente_producto_empleado():
    session = get_session()
    venta = session.query(Sale).first()
    if venta:
        assert venta.customer is not None
        assert isinstance(venta.customer, Customer)

        assert venta.product is not None
        assert isinstance(venta.product, Product)

        assert venta.employee is not None
        assert isinstance(venta.employee, Employee)
