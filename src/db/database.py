from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
import threading

Base = declarative_base()


class DBConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.engine = create_engine(DATABASE_URL, echo=True)
                    cls._instance.Session = scoped_session(
                        sessionmaker(bind=cls._instance.engine)
                    )
        return cls._instance


def get_session():
    return DBConnection().Session()
