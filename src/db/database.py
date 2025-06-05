from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
import pandas as pd
from src.utils.logger import logger

Base = declarative_base()


class DBConnection:    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.engine = create_engine(DATABASE_URL, echo=True)
                cls._instance.Session = scoped_session(
                    sessionmaker(bind=cls._instance.engine)
                )
            except Exception as e:
                raise RuntimeError(f"Error al conectar a la base de datos: {str(e)}")
        return cls._instance

    def get_session(self):
        try:
            logger.info("Obteniendo sesión de la base de datos...")
            return self.Session()
        except Exception as e:
            logger.error(f"Error al obtener la sesión: {str(e)}")
            return None

    def close_session(self, session):
        try:
            logger.info("Cerrando sesión de la base de datos...")
            session.close()
        except Exception as e:
            logger.error(f"Error al cerrar la sesión: {str(e)}")

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la consulta: {str(e)}")
