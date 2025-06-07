import pandas as pd
import pytest
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
        "EmployeeName": ["Alice Smith", "Bob Johnson", "Alice Smith", "Charlie Brown", "Bob Johnson"],
        "TotalPrice": [100, 200, 150, 300, 250],
        "ProductID": [101, 102, 103, 104, 105],
        "ProductName": ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer"],
        "Quantity": [1, 2, 1, 3, 1],
        "CustomerID": [201, 202, 203, 204, 205],
        "CustomerName": ["John Doe", "Jane Smith", "Alice Brown", "Bob White", "Charlie Green"],
    }
    return pd.DataFrame(data)


def test_product_sales_by_employee(sample_sales_data):
    """
    Test para verificar la generación de un informe de ventas por empleado,
    mostrando las ventas totales por producto.
    
    Primero testea que el informe contiene las columnas esperadas,
    luego verifica que no esté vacío.
    por ultimo, comprueba que el informe tiene la cantidad correcta de filas.

    """

    strategy = ProductSalesByEmployee()
    report = strategy.generate_report(sample_sales_data, key="EmployeeName", ascending=False)

    expected_columns = ["IDVendedor", "Nombre Apellido Vendedor", "Cantidad de productos vendidos"]

    assert list(report.columns) == expected_columns, (
        f"Se esperaban: {expected_columns}, pero se obtuvieron: {list(report.columns)}"
    )

    assert not report.empty, "El informe de ventas por producto está vacío."

    assert len(report) == 3, (
        "El informe de ventas por producto debe contener 3 filas, una por cada vendedor."
    )


def test_product_by_employee_sorting_by_name(sample_sales_data):
    """
    Test para verificar que el informe de ventas por empleado se ordena correctamente 
    por nombre de empleado.
    """
    strategy = ProductSalesByEmployee()
    report = strategy.generate_report(sample_sales_data, key="EmployeeName", ascending=True)

    # Verifica que el informe esté ordenado por nombre de empleado
    assert report["Nombre Apellido Vendedor"].is_monotonic_increasing, (
        "El informe no está ordenado correctamente por nombre de empleado."
    )


def test_product_by_employee_sorting_by_total_price(sample_sales_data):
    """
    Test para verificar que el informe de ventas por empleado se ordena correctamente 
    por precio total.
    """
    strategy = ProductSalesByEmployee()
    report = strategy.generate_report(sample_sales_data, key="ProductID", ascending=False)

    # Verifica que el informe esté ordenado por cantidad de productos vendidos
    assert report["Cantidad de productos vendidos"].is_monotonic_decreasing, (
        "El informe no está ordenado correctamente por cantidad de productos vendidos."
    )


def test_total_sales_by_employee(sample_sales_data):
    """
    Test para verificar la generación de un informe de ventas totales por empleado.
    
    Primero testea que el informe contiene las columnas esperadas,
    luego verifica que no esté vacío.
    por ultimo, comprueba que el informe tiene la cantidad correcta de filas.
    """
    strategy = TotalSalesByEmployee()
    report = strategy.generate_report(sample_sales_data, key="TotalPrice", ascending=False)

    expected_columns = ["IDVendedor", "Nombre Apellido Vendedor", "TotalVentas"]

    assert list(report.columns) == expected_columns, (
        f"Se esperaban: {expected_columns}, pero se obtuvieron: {list(report.columns)}"
    )

    assert not report.empty, "El informe de ventas totales está vacío."

    assert len(report) == 3, (
        "El informe de ventas totales debe contener 3 filas, una por cada vendedor."
    )

def test_average_sales_by_employee(sample_sales_data):
    """
    Test para verificar la generación de un informe de ventas promedio por empleado.
    Primero testea que el informe contiene las columnas esperadas,
    luego verifica que no esté vacío.
    por ultimo, comprueba que el informe tiene la cantidad correcta de filas.
    """
    strategy = AverageSalesByEmployee()
    report = strategy.generate_report(sample_sales_data, key="TotalPrice", ascending=False)

    expected_columns = ["IDVendedor", "Nombre Apellido Vendedor", "Promedio de ventas"]

    assert list(report.columns) == expected_columns, (
        f"Se esperaban: {expected_columns}, pero se obtuvieron: {list(report.columns)}"
    )

    assert not report.empty, "El informe de ventas promedio está vacío."

    assert len(report) == 3, (
        "El informe de ventas promedio debe contener 3 filas, una por cada vendedor."
    )