from abc import ABC, abstractmethod


class BaseFactory(ABC):
    """
    Clase base abstracta para fabricas que define el método from_series.
    Las clases que hereden de BaseFactory deben implementar este método para crear instancias
    """

    @abstractmethod
    def from_series(self, serie):
        pass


class SalesSummary(BaseFactory):
    """
    Esta clase devuelve un resumen de las ventas con el nombre del producto, el nombre del cliente,
    el nombre del empleado, la cantidad vendida y el precio total de la venta,
    a partir de un DataFrame de ventas.
    Antes de usar esta clase, asegúrate de que el DataFrame contiene las columnas necesarias.

    Ejemplo de query para obtener los datos (usar en Jupyter Notebook o similar):

    ```sql
    select SalesID, s.ProductID, ProductName, Quantity, TotalPrice, c.CustomerID, coalesce(concat(c.FirstName, " ", c.MiddleInitial, ". ", c.LastName), "Sin nombre") as CustomerName,
    e.EmployeeID, concat(e.FirstName, " ", e.MiddleInitial, ". ", e.LastName) as EmployeeName
    from sales s join products p on s.productid = p.ProductID
    join customers c on s.CustomerID = c.CustomerID
    join employees e on s.SalesPersonID = e.EmployeeID
    order by c.CustomerID;
    ```

    Args:
        sale_id (int): ID de la venta.
        product_id (int): ID del producto vendido.
        product_name (str): Nombre del producto vendido.
        quantity (int): Cantidad de productos vendidos.
        total_price (float): Precio total de la venta.
        customer_id (int): ID del cliente.
        customer_name (str): Nombre del cliente.
        employee_id (int): ID del empleado que realizó la venta.
        employee_name (str): Nombre del empleado que realizó la venta.

    Methods:
        from_series(serie): Crea una instancia de SalesSummary a partir de una serie de datos.

    Usage:
        sales_summary = SalesSummary.from_series(serie)

    returns:
        SalesSummary: Una instancia de la clase SalesSummary con los datos de la venta.
    """

    def __init__(
        self,
        sale_id,
        product_id,
        product_name,
        quantity,
        total_price,
        customer_id,
        customer_name,
        employee_id,
        employee_name,
    ):
        self.sale_id = sale_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.total_price = total_price

    @classmethod
    def from_series(cls, serie):
        return cls(
            sale_id=serie["SalesID"],
            product_id=serie["ProductID"],
            product_name=serie["ProductName"],
            quantity=serie["Quantity"],
            total_price=serie["TotalPrice"],
            customer_id=serie["CustomerID"],
            customer_name=serie["CustomerName"],
            employee_id=serie["EmployeeID"],
            employee_name=serie["EmployeeName"],
        )


class CustomerLocationInfo(BaseFactory):
    """
    Esta clase devuelve la información del cliente a partir de un DataFrame de clientes.
    Antes de usar esta clase, asegúrate de que el DataFrame contiene las columnas necesarias.

    Ejemplo de query para obtener los datos (usar en Jupyter Notebook o similar):
    ```sql
    select SalesID, s.ProductID, ProductName, Quantity, TotalPrice, c.CustomerID, coalesce(concat(c.FirstName, " ", c.MiddleInitial, ". ", c.LastName), "Sin nombre") as CustomerName,
    e.EmployeeID, concat(e.FirstName, " ", e.MiddleInitial, ". ", e.LastName) as EmployeeName
    from sales s join products p on s.productid = p.ProductID
    join customers c on s.CustomerID = c.CustomerID 
    join employees e on s.SalesPersonID = e.EmployeeID
    order by c.CustomerID;
    ```

    Args:
        customer_id (int): ID del cliente.
        first_name (str): Nombre del cliente.
        middle_initial (str): Inicial del segundo nombre del cliente.
        last_name (str): Apellido del cliente.
        address (str): Dirección del cliente.
        city_name (str): Ciudad del cliente.
        state_name (str): Estado del cliente.
        country_name (str): País del cliente.

    Methods:
        from_series(serie): Crea una instancia de CustomerLocationInfo a partir de una serie de datos.

    Usage:
        customer_location = CustomerLocationInfo.from_series(serie)

    returns:
        CustomerLocationInfo: Una instancia de la clase CustomerLocationInfo con los datos del cliente.
    """

    def __init__(
        self,
        customer_id,
        first_name,
        middle_initial,
        last_name,
        address,
        city_name,
        country_name,
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.address = address
        self.city_name = city_name
        self.country_name = country_name

    @classmethod
    def from_series(cls, serie):
        return cls(
            customer_id=serie["CustomerID"],
            first_name=serie["FirstName"],
            middle_initial=serie["MiddleInitial"],
            last_name=serie["LastName"],
            address=serie["Address"],
            city_name=serie["CityName"],
            country_name=serie["CountryName"],
        )
