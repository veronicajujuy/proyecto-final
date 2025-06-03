from src.models.customer import Customer
from src.models.employee import Employee
from src.models.product import Product
from src.models.sale import Sale
from abc import ABC, abstractmethod


class BaseFactory(ABC):
    @abstractmethod
    def from_series(self, serie):
        pass


class CustomerFactory(BaseFactory):
    @staticmethod
    def from_series(serie):
        return Customer(
            CustomerID=serie["CustomerID"],
            FirstName=serie["FirstName"],
            MiddleInitial=serie["MiddleInitial"],
            LastName=serie["LastName"],
            CityID=serie["CityID"],
            Address=serie["Address"],
        )


class EmployeeFactory(BaseFactory):
    @staticmethod
    def from_series(serie):
        return Employee(
            EmployeeID=serie["EmployeeID"],
            FirstName=serie["Firstname"],
            MiddleInitial=serie["MiddleInitial"],
            LastName=serie["LastName"],
            BirthDate=serie["BirthDate"],
            Gender=serie["Gender"],
            CityID=serie["CityID"],
            HireDate=serie["HireDate"],
        )


class ProductFactory(BaseFactory):
    @staticmethod
    def from_series(serie):
        return Product(
            ProductID=serie["ProductID"],
            ProductName=serie["ProductName"],
            CategoryID=serie["CategoryID"],
            UnitPrice=serie["UnitPrice"],
        )


class SaleFactory(BaseFactory):
    @staticmethod
    def from_series(serie):
        return Sale(
            SaleID=serie["SaleID"],
            ProductID=serie["ProductID"],
            CustomerID=serie["CustomerID"],
            EmployeeID=serie["EmployeeID"],
            OrderDate=serie["OrderDate"],
            Quantity=serie["Quantity"],
            TotalPrice=serie["TotalPrice"],
        )
