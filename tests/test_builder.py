import pandas as pd
import pytest
from src.design_patterns.builder import ReportBuilder
from src.design_patterns.strategy import (
    TotalSalesByEmployee,
    ProductSalesByEmployee,
    AverageSalesByEmployee,
)


@pytest.fixture
def sample_sales_data():
    """
    Fixture para proporcionar un DataFrame de ventas de ejemplo.
    Este DataFrame debe contener las columnas necesarias para generar informes.
    """
    data = {
        "EmployeeID": [1, 2, 1, 3, 2],
        "EmployeeName": [
            "Alice Smith",
            "Bob Johnson",
            "Alice Smith",
            "Charlie Brown",
            "Bob Johnson",
        ],
        "TotalPrice": [100, 200, 150, 300, 250],
        "ProductID": [101, 102, 103, 104, 105],
        "ProductName": ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer"],
        "Quantity": [1, 2, 1, 3, 1],
        "CustomerID": [201, 202, 203, 204, 205],
        "CustomerName": [
            "John Doe",
            "Jane Smith",
            "Alice Brown",
            "Bob White",
            "Charlie Green",
        ],
    }
    return pd.DataFrame(data)


def test_report_builder_add_report(sample_sales_data):
    """
    Test para verificar que el ReportBuilder puede agregar diferentes estrategias de informes
    y generar un informe final a partir de un DataFrame de pandas.

    Este test verifica que se pueden agregar múltiples estrategias de informes,
    y que el informe final contiene datos.
    Además, comprueba que el informe combinado está ordenado correctamente por nombre de empleado.
    """
    builder = ReportBuilder()

    reports = (
        builder.set_dataframe(sample_sales_data)
        .set_combined_sorting("EmployeeName", True)
        .add_report(TotalSalesByEmployee())
        .add_report(AverageSalesByEmployee())
        .add_report(ProductSalesByEmployee())
        .build_all()
    )


    assert len(reports) == 4, "Se esperaban 4 informes, uno por cada estrategia."

    for key, report in reports.items():
        assert isinstance(report, pd.DataFrame), (
            f"El informe '{key}' no es un DataFrame."
        )
        assert not report.empty, f"El informe '{key}' está vacío."

    report_combined = reports["CombinedReport"]

    assert report_combined["Nombre Apellido Vendedor"].is_monotonic_increasing, (
        "El informe no está ordenado correctamente por nombre de vendedor."
    )
