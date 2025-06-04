from abc import ABC, abstractmethod
import pandas as pd


class ReportStrategy(ABC):
    @abstractmethod
    def generate_report(self, data: pd.DataFrame, key) -> pd.DataFrame:
        pass


class TotalSalesByEmployee(ReportStrategy):
    def generate_report(self, df,key):
        ventas = (
            df.groupby("SalesPersonID")[["TotalPrice"]]
            .sum()
            .sort_values(key, ascending=False)
        )
        nombres = df[["SalesPersonID", "Firstname", "LastName"]].drop_duplicates(
            subset="SalesPersonID"
        )

        resultado = ventas.merge(nombres, on="SalesPersonID", how="left")

        resultado = resultado[["SalesPersonID", "Firstname", "LastName", "TotalPrice"]]
        resultado.sort_values(key, ascending=False, inplace=True)
        resultado.columns = ["IDVendedor", "Nombre", "Apellido", "TotalVentas"]

        return resultado


class AverageSalesByEmployee(ReportStrategy):
    def generate_report(self, df, key):
        ventas = (
            df.groupby("SalesPersonID")[["TotalPrice"]]
            .mean()
            .round(2)
            .sort_values(key, ascending=False)
        )
        nombres = df[["SalesPersonID", "Firstname", "LastName"]].drop_duplicates(
            subset="SalesPersonID"
        )

        resultado = ventas.merge(nombres, on="SalesPersonID", how="left")

        resultado = resultado[["SalesPersonID", "Firstname", "LastName", "TotalPrice"]]
        resultado.sort_values(key, ascending=False, inplace=True)
        resultado.columns = ["IDVendedor", "Nombre", "Apellido", "Promedio de ventas"]

        return resultado


class TopProductSalesByEmployee(ReportStrategy):
    def generate_report(self, df, key):
        ventas = (
            df.groupby("SalesPersonID")[["ProductID"]]
            .count()
            .sort_values(key, ascending=False)
        )
        nombres = df[["SalesPersonID", "Firstname", "LastName"]].drop_duplicates(
            subset="SalesPersonID"
        )

        resultado = ventas.merge(nombres, on="SalesPersonID", how="left")

        resultado = resultado[["SalesPersonID", "Firstname", "LastName", "ProductID"]]
        resultado.sort_values(key, ascending=False, inplace=True)
        resultado.columns = ["IDVendedor", "Nombre", "Apellido", "Producto mas vendido"]

        return resultado
