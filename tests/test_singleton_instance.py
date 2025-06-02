from src.db.database import DBConnection


def test_singleton_instance():
    db1 = DBConnection()
    db2 = DBConnection()

    assert db1 is db2
    assert db1.engine is db2.engine
    assert db1.Session is db2.Session
