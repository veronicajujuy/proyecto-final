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
    """
    Prueba unitaria para verificar la consulta de una entidad en la base de datos.
    Esta prueba asegura que al consultar la primera instancia de una entidad,
    se obtenga un objeto del tipo esperado o None si no hay instancias.
    """

    nombre, clase = model
    db = DBConnection()
    session = db.get_session()
    try:
        instancia = session.query(clase).first()
        logger.info(f"instancia: {instancia}")
        assert instancia is None or isinstance(instancia, clase)
    except Exception as e:
        pytest.fail(f"{nombre} falló con error: {str(e)}")
