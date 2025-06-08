from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
import pandas as pd
from src.utils.logger import logger

Base = declarative_base()


class DBConnection:
    """
    Clase para manejar la conexión a la base de datos.
    Esta clase implementa el patrón Singleton para asegurar que solo haya una instancia de conexión a la base de datos.
    Permite ejecutar consultas SQL y obtener resultados en forma de DataFrame de pandas.

    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.engine = create_engine(DATABASE_URL, echo=False)
                cls._instance.Session = scoped_session(
                    sessionmaker(bind=cls._instance.engine)
                )
            except Exception as e:
                raise RuntimeError(f"Error al conectar a la base de datos: {str(e)}")
        return cls._instance

    def get_session(self):
        """
        Obtiene una nueva sesión de la base de datos utilizando SQLAlchemy.

        Utiliza la instancia única (Singleton) de la clase DBConnection para crear y devolver una sesión.
        Es útil para operaciones ORM que requieren una sesión activa.

        Returns:
            Session: Una instancia de sesión de SQLAlchemy para interactuar con la base de datos.
            None: Si ocurre un error al obtener la sesión.

        Ejemplo:
            >>> db = DBConnection()
            >>> session = db.get_session()
        """
        try:
            logger.info("Obteniendo sesión de la base de datos...")
            return self.Session()
        except Exception as e:
            logger.error(f"Error al obtener la sesión: {str(e)}")
            return None

    def close_session(self, session):
        """
        Cierra una sesión activa de la base de datos.

        Este método debe llamarse después de finalizar las operaciones con la sesión para liberar recursos.

        Args:
            session (Session): La sesión de SQLAlchemy que se desea cerrar.

        Ejemplo:
            >>> db = DBConnection()
            >>> session = db.get_session()
            >>> # ... realizar operaciones ...
            >>> db.close_session(session)
        """
        try:
            logger.info("Cerrando sesión de la base de datos...")
            session.close()
        except Exception as e:
            logger.error(f"Error al cerrar la sesión: {str(e)}")

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL sobre la base de datos y devuelve los resultados como un DataFrame de pandas.
        Esta función permite ejecutar consultas SQL parametrizadas, lo que ayuda a prevenir inyecciones SQL.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (dict, opcional): Diccionario de parámetros para la consulta SQL. Por defecto es None.

        Returns:
            pd.DataFrame: Un DataFrame de pandas que contiene los resultados de la consulta, con los nombres de las columnas correspondientes.

        Raises:
            RuntimeError: Si ocurre un error durante la ejecución de la consulta o la conexión a la base de datos.

        Ejemplo:
            >>> db = DBConnection()
            >>> df = db.execute_query("SELECT * FROM employees WHERE id = :id", {"id": 1})
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la consulta: {str(e)}")

    def call_procedure(self, name: str, args: list = None) -> pd.DataFrame:
        """
        Ejecuta un stored procedure y devuelve el último result set como DataFrame.
        """
        raw = self.engine.raw_connection()
        try:
            cursor = raw.cursor()
            cursor.callproc(name, args or [])
            rows, cols = [], []
            for rs in cursor.stored_results():
                rows = rs.fetchall()
                cols = rs.column_names
            return pd.DataFrame(rows, columns=cols)
        finally:
            cursor.close()
            raw.close()

    def query_view(
        self, view_name: str, where: str = None, params: dict = None
    ) -> pd.DataFrame:
        """
        Hace un SELECT * desde una vista (o tabla), opcionalmente filtrando.
        """
        sql = f"SELECT * FROM {view_name}"
        if where:
            sql += f" WHERE {where}"
        # Usa execute_query para todo el trabajo
        return self.execute_query(sql, params)

    def execute_ddl(self, query: str):
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar DDL: {e}")
