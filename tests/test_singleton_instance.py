from src.db.database import DBConnection


def test_singleton_instance():
    """
    Prueba unitaria para verificar que la clase DBConnection implementa correctamente el patrón Singleton.
    Esta prueba asegura que todas las instancias de DBConnection son la misma,
    """
    db1 = DBConnection()
    db2 = DBConnection()

    assert db1 is db2
    assert db1.engine is db2.engine
    assert db1.Session is db2.Session
