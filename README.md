# Proyecto Final - Data Engineering

## 🛠️ Características Implementadas

- 📄 **Modelado relacional en MySQL**:  
  Base de datos `sales_company` con tablas normalizadas, claves primarias y relaciones que mantienen la integridad referencial.
  Se implementó el mapeo de todas las clases modeladas a las ya cargadas en la base de datos.

- 🔌 **Conexión a base de datos con SQLAlchemy**:  
  Implementación del patrón Singleton para asegurar una única instancia de conexión a la base de datos, optimizando recursos.

- 🧠 **Patrones de Diseño**:
  - **Singleton**: Conexión a base de datos única y centralizada.
  - **Factory**: Creación de objetos `SalesSummary` y `CustomerLocationInfo` a partir de DataFrames.
  - **Strategy**: Generación de reportes específicos de ventas (totales, promedios, productos).
  - **Builder**: Construcción flexible de reportes combinados a partir de estrategias individuales.

- 📊 **Análisis de datos en Jupyter Notebook**:  
  Consultas SQL complejas convertidas a DataFrames de pandas, visualización y generación de reportes.

- ✅ **Pruebas unitarias con pytest**:  
  Tests exhaustivos para:
  - Patrones de diseño (Singleton, Factory, Strategy, Builder)
  - Validación de relaciones ORM
  - Verificación de integridad de datos

---

## 📁 Estructura del Proyecto

```
proyecto_final/
├── src/
│   ├── db/
│   │   └── database.py        # Conexión a BD con patrón Singleton
│   ├── models/               # Modelos ORM
│   │   ├── category.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── employee.py
│   │   └── sale.py
│   ├── design_patterns/
│   │   ├── factory.py        # Patrón Factory
│   │   ├── strategy.py       # Patrón Strategy
│   │   └── builder.py        # Patrón Builder
│   └── utils/
│       └── logger.py         # Sistema de logs configurado
│
├── tests/
│   ├── test_singleton_instance.py  # Tests para patrón Singleton
│   ├── test_factory.py            # Tests para patrón Factory
│   ├── test_strategy.py           # Tests para patrón Strategy
│   ├── test_builder.py            # Tests para patrón Builder
│   └── test_tablas_base_datos.py  # Tests para relaciones ORM
│
├── config.py                 # Configuración centralizada
├── main.ipynb                # Notebook con implementación y demostraciones
└── README.md                 # Documentación del proyecto
```
---

## Desarrollo

- 🧩 **Modelos ORM con SQLAlchemy**:  
  Clases `Product`, `Customer`, `Sale`, `Country`, `City`, `Employee` y `Category` que implementan patrones OOP:
  - Abstracción de tablas como objetos Python
  - Relaciones entre entidades a través de `relationship`
  - Documentación completa mediante docstrings

## 💡 Implementación de Patrones de Diseño

### 🔄 Patrón Singleton
Aplicado en `DBConnection` para garantizar una única instancia de conexión a la base de datos:
```python
# Ejemplo simplificado
class DBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL)
        return cls._instance
```

### 🔄 Patrón Factory

Implementado en `SalesSummary` y `CustomerLocationInfo` para crear objetos estructurados dede un DataFrame

```python
# Ejemplo de uso
sales = [SalesSummary.from_series(row) for _, row in df_sales.iterrows()]

```

### 🔄 Patrón Strategy

Define diferentes algoritmos de generación de reportes intercambiables

Estrategias Disponibles: `TotalSalesEmployee`, `AverageSalesByEmployee` y `ProductSalesByEmployee`

```python
# Ejemplo de uso
report = TotalSalesByEmployee()
report.generate_report(df_sales, "EmployeeName")

```
### 🔄 Patrón Builder

Utiliza las estrategias del patrón strategy y arma un reporte completo. También se pueden armar reportes individuales

```python
# Ejemplo de uso
builder = ReportBuilder()

reports = (
    builder.set_dataframe(df_sales)
    .set_combined_sorting("EmployeeName", True)
    .add_report(TotalSalesByEmployee())
    .add_report(AverageSalesByEmployee())
    .add_report(ProductSalesByEmployee())
    .build_all()
)

# Reporte combinado que integra todos los reportes individuales
reports["CombinedReport"] 

```

### 📝 Consultas implementadas

El proyecto incluye consultas SQL complejas ejecutadas y convertidas en dataframes

```python
# Ejemplo de query transformada a DataFrame
query = """
select SalesID, s.ProductID, ProductName, Quantity, TotalPrice, 
       c.CustomerID, concat(c.LastName, ", ", c.FirstName) as CustomerName,
       e.EmployeeID, concat(e.LastName, ", ", e.FirstName) as EmployeeName
from sales s 
join products p on s.productid = p.ProductID
join customers c on s.CustomerID = c.CustomerID 
join employees e on s.SalesPersonID = e.EmployeeID
"""
df_sales = db.execute_query(query)

```

## 🧪 Pruebas Unitarias

Tests realizados en Jupiter Notebook

- **Tests para patrones de diseño**:
  - Singleton: Verificación de instancia única.
  - Factory: Creación correcta de objetos desde Series de pandas.
  - Strategy: Validación de cálculos y estructura de reportes.
  - Builder: Comprobación de la construcción y combinación de reportes.

Tests realizados para ser ejecutados en consola

- **Tests para modelos ORM**:
  - Verificación de relaciones (cliente-ciudad, producto-categoría).
  - Validación de atributos y tipos de datos.
  - Integridad de datos entre tablas relacionadas.


## 👩‍💻 Autor

Proyecto desarrollado por Veronica Valdez como parte del Proyecto Final del Curso Data Engineering