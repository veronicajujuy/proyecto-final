# Proyecto Final - Data Engineering
## Avance 2

## 🛠️ Características Implementadas

- 📄 **Modelado relacional en MySQL**:  
  Base de datos `sales_company` con tablas normalizadas, claves primarias y relaciones que mantienen la integridad referencial.
  Se implementó el mapeo de todas las clases modeladas a las ya cargadas en la base de datos.

- 🔌 **Conexión a base de datos con SQLAlchemy**:  
  Implementación del patrón **Singleton** en la clase `DBConnection` para asegurar una única instancia de conexión y administración de sesiones en todo el sistema, previniendo duplicidad de conexiones y problemas de concurrencia.  
  Se utiliza `scoped_session` para gestionar sesiones de forma segura incluso en posibles entornos multi-hilo o múltiples kernels (Jupyter/consola).

- 🧠 **Patrones de Diseño**:
  - **Singleton**: Única instancia de conexión a la base.
  - **Factory**: Construcción de objetos `SalesSummary` y `CustomerLocationInfo` a partir de Series de pandas, desacoplando la lectura de datos de su uso en lógica de negocio y presentación.
  - **Strategy**: Generación flexible de distintos tipos de reportes (totales, promedios, conteos) a partir del mismo DataFrame.
  - **Builder**: Armado fluido y declarativo de reportes combinados o individuales, encadenando estrategias de análisis.

- 📊 **Análisis de datos en Jupyter Notebook**:  
  Consultas SQL complejas convertidas a DataFrames de pandas, visualización y generación de reportes.

- ✅ **Pruebas unitarias con pytest**:  
  - Validación de patrones de diseño (Singleton, Factory, Strategy, Builder)
  - Pruebas sobre el mapeo ORM y las relaciones entre entidades
  - Chequeo de integridad y consistencia de los datos

---

## 📁 Estructura del Proyecto

```css
proyecto_final/
├── data/
│   │   └── categories.csv        # archivos .csv
│   │   └── ...
│   │   └── sales.csv
├── sql/
│   │   └── load_data.sql        # script para cargar los .csv a la base de datos
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
  Las clases `Product`, `Customer`, `Sale`, `Country`, `City`, `Employee` y `Category` mapean las tablas existentes de MySQL y aplican POO:
- **Abstracción**: Cada tabla se representa como una clase Python.
- **Relaciones**: Se utilizan `relationship` y claves foráneas para modelar las asociaciones entre entidades (por ejemplo, cliente-ciudad, venta-producto-empleado).
- **Documentación y claridad**: Cada clase y atributo incluye docstrings para facilitar su uso y extensión.

## 💡 Implementación de Patrones de Diseño

### 🔄 Patrón Singleton
Aplicado en `DBConnection` para garantizar una única instancia de conexión a la base de datos:
```python
class DBConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL)
            cls._instance.Session = scoped_session(sessionmaker(bind=cls._instance.engine))
        return cls._instance
```

### 🔄 Patrón Factory

Las clases `SalesSummary` y `CustomerLocationInfo` aplican Factory para crear objetos de dominio a partir de filas de un DataFrame

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

El sistema ejecuta queries avanzadas, transformando los resultados en DataFrames para análisis y visualización:

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

## 🔐 Seguridad y mejores prácticas
- Variables de entorno y archivo `.env`:
Todas las credenciales y datos sensibles se almacenan en `.env` y nunca se suben al repositorio (.gitignore), siguiendo buenas prácticas de seguridad y preparación para despliegues reales.

## 👩‍💻 Autor

Proyecto desarrollado por Veronica Valdez como parte del Proyecto Final del Curso Data Engineering