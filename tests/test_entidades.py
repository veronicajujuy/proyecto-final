import pytest
from src.db.database import DBConnection
from src.models import Country, City, Category, Product, Customer, Employee, Sale
from src.utils.logger import logger


@pytest.mark.parametrize(
    "model",
    [
        ("Country", Country),
        ("City", City),
        ("Category", Category),
        ("Product", Product),
        ("Customer", Customer),
        ("Employee", Employee),
        ("Sale", Sale),
    ],
)
def test_entidad_consulta(model):
    nombre, clase = model
    db = DBConnection()
    session = db.get_session()
    try:
        instancia = session.query(clase).first()
        logger.info(f"instancia: {instancia}")
        assert instancia is None or isinstance(instancia, clase)
    except Exception as e:
        pytest.fail(f"{nombre} falló con error: {str(e)}")
