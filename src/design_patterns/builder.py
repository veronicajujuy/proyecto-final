import pandas as pd
from src.design_patterns.strategy import ReportStrategy
from src.utils.logger import logger


class ReportBuilder:
    """
         Clase para construir informes utilizando el patrón Builder.
    Permite agregar diferentes estrategias de informes y generar un informe final
    a partir de un DataFrame de pandas, además de un informe combinado.

    Modelo de uso:
        builder = ReportBuilder()

        reports = (
            builder.set_dataframe(df_sales)
            .set_combined_sorting("EmployeeName", True)
            .add_report(TotalSalesByEmployee())
            .add_report(AverageSalesByEmployee())
            .add_report(ProductSalesByEmployee())
            .build_all()
        )
    """

    def __init__(self):
        self.df = None
        self._report_configs = []
        self.combined_sort_key = None
        self.combined_sort_ascending = True

    def set_dataframe(self, df: pd.DataFrame):
        """
        Establece el DataFrame a utilizar en los informes.
        """
        self.df = df
        return self

    def set_combined_sorting(self, key: str, ascending: bool = True):
        """
        Establece la clave y el orden de clasificación para el informe combinado.
        key debe ser el nombre EXACTO de la columna en el DataFrame combinado
        """
        self.combined_sort_key = key
        self.combined_sort_ascending = ascending
        return self

    def add_report(self, strategy: ReportStrategy):
        """
        Agrega una nueva estrategia de reporte junto con su clave de ordenamiento.
        Cada estrategia usa su propia // clave (key) y ascendente (ascending)
        para ordenar el DataFrame que ella produce.
        """
        if self.df is None:
            raise ValueError("Debe existir un DataFrame antes de agregar informes.")
        self._report_configs.append(strategy)
        return self

    def build_all(self):
        """
        Genera todos los reportes individuales según las estrategias cargadas,
        y luego construye un 'CombinedReport' uniendo con merge todos los resultados.
        
        Devuelve un diccionario donde:
            - keys son los nombres de cada estrategia (e.j. "TotalSalesByEmployee")
            - value es el DataFrame producido por esa estrategia.
        También añade "CombinedReport" al final.
        """
        if self.df is None or not self._report_configs:
            raise ValueError("Falta un DataFrame o una configuración de informe.")

        result = {}
        combine_reports = None

        for strategy in self._report_configs:
            name = strategy.__class__.__name__

            report = strategy.generate_report(
                self.df,
                key=self.combined_sort_key,
                ascending=self.combined_sort_ascending,
            )
            result[name] = report

            if combine_reports is None:
                combine_reports = report
            else:
                combine_reports = pd.merge(
                    combine_reports, report, on="IDVendedor", how="outer"
                )

            result["CombinedReport"] = self._clean_combined_df(combine_reports)

        return result

    def _clean_combined_df(self, df: pd.DataFrame):
        """
        Metodo privado que limpia el DataFrame combinado eliminando columnas duplicadas y renombrando las columnas de IDVendedor.
        """
        name_columns = [col for col in df.columns if "Nombre Apellido Vendedor" in col]

        if len(name_columns) > 1:
            main_col = name_columns[0]
            for col in name_columns[1:]:
                df[main_col] = df[main_col].fillna(df[col])  # combinamos si hay nulos
                df.drop(columns=col, inplace=True)

            df.rename(columns={main_col: "Nombre Apellido Vendedor"}, inplace=True)

            df = df.sort_values(
                "Nombre Apellido Vendedor", ascending=self.combined_sort_ascending
            ).reset_index(drop=True)

        return df
