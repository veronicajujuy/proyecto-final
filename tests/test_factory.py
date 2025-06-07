import pandas as pd
import pytest
from src.design_patterns.factory import SalesSummary, CustomerLocationInfo


@pytest.fixture
def samples_sales_data_series():
    """
    Fixture para proporcionar una serie de datos de ventas de ejemplo.
    Esta serie debe contener las columnas necesarias para crear una instancia de SalesSummary.
    """
    data = {
        "SalesID": 101,
        "ProductID": 202,
        "ProductName": "Laptop Gamer",
        "Quantity": 1,
        "TotalPrice": 1500.75,
        "CustomerID": 303,
        "CustomerName": "Ana Torres",
        "EmployeeID": 404,
        "EmployeeName": "Carlos Ruiz",
    }
    return pd.Series(data)


def test_sales_summary_creation(samples_sales_data_series):
    """
    Test para verificar la creación de una instancia de SalesSummary a partir de una serie de datos de ventas.
    """
    serie = samples_sales_data_series
    summary = SalesSummary.from_series(serie)

    assert isinstance(summary, SalesSummary), (
        "El objeto creado no es una instancia de SalesSummary."
    )
    assert summary.sale_id == serie["SalesID"]
    assert summary.product_id == serie["ProductID"]
    assert summary.product_name == serie["ProductName"]
    assert summary.quantity == serie["Quantity"]
    assert summary.total_price == serie["TotalPrice"]
    assert summary.customer_id == serie["CustomerID"]
    assert summary.customer_name == serie["CustomerName"]
    assert summary.employee_id == serie["EmployeeID"]
    assert summary.employee_name == serie["EmployeeName"]


@pytest.fixture
def sample_customer_location_info():
    """
    Fixture para proporcionar un DataFrame de información de ubicación de clientes de ejemplo.
    Este DataFrame debe contener las columnas necesarias para crear una instancia de CustomerLocationInfo.
    """
    data = {
        "CustomerID": 505,
        "FirstName": "Luisa",
        "MiddleInitial": "M",
        "LastName": "Perez",
        "Address": "Calle Falsa 123",
        "CityName": "Springfield",
        "CountryName": "País de Ejemplo",
    }
    return pd.Series(data)


def test_customer_location_info_creation(sample_customer_location_info):
    """
    Test para verificar la creación de una instancia de CustomerLocationInfo a partir de un DataFrame de clientes.
    """
    serie = sample_customer_location_info
    info = CustomerLocationInfo.from_series(serie)

    assert isinstance(info, CustomerLocationInfo), (
        "El objeto creado no es una instancia de CustomerLocationInfo."
    )
    assert info.customer_id == serie["CustomerID"]
    assert info.first_name == serie["FirstName"]
    assert info.middle_initial == serie["MiddleInitial"]
    assert info.last_name == serie["LastName"]
    assert info.address == serie["Address"]
    assert info.city_name == serie["CityName"]
    assert info.country_name == serie["CountryName"]


def test_customer_location_info_missing_columns():
    """
    Test para verificar el manejo de un DataFrame de clientes que falta alguna columna necesaria.
    """
    data = {
        "CustomerID": 505,
        "FirstName": "Luisa",
        "LastName": "Perez",
        # Falta 'MiddleInitial', 'Address', 'CityName', 'CountryName'
    }
    serie = pd.Series(data)

    with pytest.raises(KeyError):
        CustomerLocationInfo.from_series(serie)  # Debe lanzar un KeyError por columnas faltantes
