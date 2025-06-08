from abc import ABC, abstractmethod
import pandas as pd


class ReportStrategy(ABC):
    """
    Clase base abstracta que define estrategias de generación de informes.
    """

    @abstractmethod
    def generate_report(self, data: pd.DataFrame, key, ascending: bool) -> pd.DataFrame:
        """
        data: DataFrame con datos originales de ventas.
        key: nombre de la columna sobre la que ordenar.
        ascending: orden ascendente (True) o descendente (False).
        Devuelve un DataFrame procesado para el informe.
        """
        pass


class TotalSalesByEmployee(ReportStrategy):
    """
    Esta clase genera un informe de ventas por cada vendedor, mostrando por cada uno el total de ventas realizadas.

    Args:
        df (pd.DataFrame): DataFrame que contiene las ventas,
        con columnas "EmployeeID", "TotalPrice" y "EmployeeName".
        key (str): Clave por la cual se ordenará el informe, puede ser "TotalPrice" o cualquier otra columna relevante.
        acscending (bool): Indica si el ordenamiento debe ser ascendente o descendente.

    Returns:
        pd.DataFrame: DataFrame con el informe de ventas por empleado,
        incluyendo "IDVendedor", "Nombre Apellido Vendedor" y "TotalVentas".
    """

    def generate_report(self, df, key, ascending=True):
        ventas = df.groupby("EmployeeID")[["TotalPrice"]].sum()
        nombres = df[["EmployeeID", "EmployeeName"]].drop_duplicates(
            subset="EmployeeID"
        )

        resultado = ventas.merge(nombres, on="EmployeeID", how="left")

        resultado = resultado[["EmployeeID", "EmployeeName", "TotalPrice"]]
        resultado.sort_values(key, ascending=ascending, inplace=True)
        resultado.columns = ["IDVendedor", "Nombre Apellido Vendedor", "TotalVentas"]

        return resultado


class AverageSalesByEmployee(ReportStrategy):
    """
    Esta clase genera un informe de ventas por vendedor, mostrando por cada uno el promedio de ventas.

    Args:
        df (pd.DataFrame): DataFrame que contiene las ventas,
        con columnas "EmployeeID", "TotalPrice" y "EmployeeName".
        key (str): Clave por la cual se ordenará el informe, puede ser "TotalPrice" o cualquier otra columna relevante.
        ascending (bool): Indica si el ordenamiento debe ser ascendente o descendente.

    Returns:
        pd.DataFrame: DataFrame con el informe de ventas por empleado,
        incluyendo "IDVendedor", "Nombre Apellido Vendedor" y "Promedio de ventas".
    """

    def generate_report(self, df, key, ascending=True):
        ventas = df.groupby("EmployeeID")[["TotalPrice"]].mean().round(2)
        nombres = df[["EmployeeID", "EmployeeName"]].drop_duplicates(
            subset="EmployeeID"
        )

        resultado = ventas.merge(nombres, on="EmployeeID", how="left")

        resultado = resultado[["EmployeeID", "EmployeeName", "TotalPrice"]]
        resultado.sort_values(key, ascending=ascending, inplace=True)
        resultado.columns = [
            "IDVendedor",
            "Nombre Apellido Vendedor",
            "Promedio de ventas",
        ]

        return resultado


class ProductSalesByEmployee(ReportStrategy):
    """
    Esta clase genera un informe de ventas por empleado, mostrando por cada uno la cantidad de productos vendidos.

    Args:
        df (pd.DataFrame): DataFrame que contiene las ventas,
        con columnas "EmployeeID", "ProductID" y "EmployeeName".
        key (str): Clave por la cual se ordenará el informe,
        puede ser por id de producto "ProductID", nombre de Empleado "EmployeeName"
        o cualquier otra columna relevante.
        ascending (bool): Indica si el ordenamiento debe ser ascendente o descendente.

    Returns:
        >>> pd.DataFrame: DataFrame con el informe de ventas por empleado,
        incluyendo "IDVendedor", "Nombre Apellido Vendedor" y "Cantidad de productos vendidos".
    """

    def generate_report(self, df, key, ascending=True):
        ventas = df.groupby("EmployeeID")[["ProductID"]].count()
        nombres = df[["EmployeeID", "EmployeeName"]].drop_duplicates(
            subset="EmployeeID"
        )

        resultado = ventas.merge(nombres, on="EmployeeID", how="left")

        resultado = resultado[["EmployeeID", "EmployeeName", "ProductID"]]
        resultado.sort_values(key, ascending=ascending, inplace=True)
        resultado.columns = [
            "IDVendedor",
            "Nombre Apellido Vendedor",
            "Cantidad de productos vendidos",
        ]

        return resultado
