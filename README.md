# Documentación Técnica - Proyecto Integrador

## Descripción General

Este documento recopila el desarrollo, las decisiones técnicas y la justificación de cada etapa del Proyecto Integrador de Análisis de Ventas.
El objetivo general es construir una solución robusta y escalable para transformar datos transaccionales en información clave para la toma de decisiones estratégicas en la empresa.

El proyecto se organiza en tres avances principales:

- Primer Avance: Modelado conceptual y diseño de la arquitectura de clases en Python**, representando las entidades principales del negocio (productos, empleados, ventas, clientes, etc.), aplicando principios de Programación Orientada a Objetos (POO) y buenas prácticas de diseño.

- Segundo Avance: Construcción y normalización del modelo relacional en MySQL, implementación de mecanismos de carga y validación de datos, y desarrollo de consultas SQL avanzadas utilizando CTEs y funciones de ventana para el análisis de ventas.

- Tercer Avance: Implementación de objetos SQL reutilizables (procedimientos almacenados y vistas), integración entre Python y la base de datos, y automatización de reportes mediante métodos y patrones de diseño que facilitan la consulta y explotación de los datos para distintos perfiles de usuario.

Cada sección documenta los pasos realizados, la justificación de las elecciones técnicas y la forma en que cada avance contribuye a una solución integral de análisis de ventas.


# **Primer Avance**

## Objetivo:

Recién incorporado al equipo de datos, se te ha asignado la tarea de sentar las bases del sistema de análisis de ventas que la dirección necesita. En esta etapa inicial, debes diseñar una arquitectura de clases en Python que represente fielmente las entidades clave del negocio, asegurando que el sistema sea sólido desde sus cimientos.

Cada decisión estructural será crucial para garantizar un sistema escalable, mantenible y alineado con los objetivos analíticos de la empresa.


## Entregables:

### Entregables realizados:

- [x] Preparación del entorno y generación del archivo requirements.txt
- [x] Creación de estructura de carpetas y archivos
- [x] Carga de datos en MySQL
- [x] Creación de clases por cada tabla y aplicación de principios de POO
- [x] Creación de prueba unitaria de testing


## Desarrollo:

### Carga de Datos en MySQL

* En el archivo sql/load_data.sql, está el script desarrollado para la carga de datos desde los archivos .csv proporcionados

**Justificación Técnica**

Cree las tablas sin Foreign Key para una carga de datos limpia. Para la carga de cada uno de los archivos .csv utilice la función** LOAD DATA INFILE **de mysql, aunque tiene la desventaja de que en la carga no se puede proporcionar una ruta relativa lo que hace difícil de migrar. 

Porque no elegí rutas relativas: Porque para utilizar LOAD DATA LOCAL INFILE, que permite el uso de rutas relativas, el script debía estar en donde guarda el SGBD MySQL (C:\ProgramData\MySQL\MySQL Server 8.0) y yo necesitaba que leyera de la carpeta en donde está el proyecto. 

Para evitar errores de importación se agregaron al script las cláusulas FIELDS TERMINATED BY ',' 

```sql
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES;
```
esta última cláusula para evitar claves ingresar claves primarias duplicadas.


### Creación de clases por cada tabla y aplicación de principios de POO

* En la carpeta src/models se encuentran cargados los modelos de cada clase:
    - `Category`, `city`, `country`, `customer`, `employee`, `product` y `sale`	

**Justificación técnica**

Como en este punto del proyecto integrador no se pedía la carga de las clases en el ORM, armé las mismas teniendo en cuenta los principios de abstracción y encapsulamiento, 


*  Cada atributo de la clase es privado y solo pueden ser accedidos a través de getter y setter apropiados, utilizando la anotación `@property` para los getters y `@atributo.setter` para el seteo de un nuevo valor del atributo. Consideré la agregación de getter y setters solo algunos atributos por clase, de acuerdo a cuales podrían ser modificados y accedidos.
* También cree funciones por cada clase, de acuerdo a la información que el cliente podría querer recuperar de las clases.
* Por ejemplo la función `get_full_name()` en customer y employee para acceder al nombre, `apply_discount()` y `is_expired()` en product y calculate_final_price() en sales.


### Creación de prueba unitaria de testing

* En la carpeta test cree dos test sobre product:
    - test_apply_discount() y test_set_negative_price() sobre funciones que cree sobre la tabla products.

**Justificación técnica**

Cree pruebas básicas para Product, con la idea de agregar más pruebas en una próxima iteración.

# **Segundo Avance**

## Objetivo

Con la base del sistema ya implementada, es momento de llevar la solución a un nuevo nivel de calidad y sostenibilidad. Se debe trabajar sobre la modularización del código y la incorporación de patrones de diseño que favorezcan la escalabilidad.

Paralelamente, la empresa necesita empezar a responder preguntas clave sobre el comportamiento de ventas, por lo que se debe construir consultas SQL avanzadas que permitan transformar grandes volúmenes de datos en información clara y útil para la toma de decisiones estratégicas.


## Entregables:

### Entregables realizados:

**Conexión a la Base de datos**

- [x] Crea una clase para conectarse a MySQL usando SQLAlchemy.
- [x] Aplica el patrón Singleton para que la conexión sea única

**Diseño e implementación**

- [x] Elige e implementa patrones de diseño relevantes
- [x] Justifica la elección de cada patrón ¿Que problema resuelve en este caso?

**Consultas desde Python**

- [x] Agrega un método en la clase de conexión que permita ejecutar consultas SQL simples
- [x] Formatea los resultados como DataFrames de Pandas

**Pruebas unitarias**

- [x] Implementa al menos una prueba unitaria con pytest enfocada en los patrones de diseño

**Seguridad de credenciales**

- [x] Guarda Credenciales de la base en un archivo .env
- [x] Asegúrate de no exponer credenciales en el código
- [x] Agrega .env al .gitignore

**Integración final**

Crea un Jupyter Notebook donde se visualice:

- [x] Conexión exitosa a la base
- [x] Resultados de las queries
- [x] Uso de los patrones de diseño
- [x] Ejecución de pruebas unitarias
- [x] Sube todo al repo


## Desarrollo

### Conexión a la Base de datos

#### Clase de Conexión a MySQL usando SQLAlchemy

Para la conexión al motor de base de datos MySQL utilicé una clase específica: DBConnection ubicada en el archivo database.py. 

Como requisito del avance implementé el patrón singleton, para asegurar que la conexión sea única y controlada desde cualquier parte del sistema.

**Implementación del patrón Singleton:**
```python
    def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                try:
                    cls._instance.engine = create_engine(DATABASE_URL, echo=False)
                    cls._instance.Session = scoped_session(
                        sessionmaker(bind=cls._instance.engine)
                    )
                except Exception as e:
                    raise RuntimeError(f"Error al conectar a la base de datos: {str(e)}")
            return cls._instance
```


**Justificación técnica**

El patrón singleton se implementa en el método `__new__` que es el que crea el objeto. Se chequea si ya existe una instancia (_instance), sino la crea. Si existe retorna la misma.

Además de la utilización del patrón singleton, utilicé una scoped_session, que administra automáticamente una sesión por hilo de ejecución y siempre usa la misma gracias al patrón Singleton. Esto evita problemas de concurrencia, especialmente si en el futuro hay varios kernels o instancias ejecutándose en paralelo (por ejemplo, en Jupyter Notebook o desde la consola).

Si bien el entorno principal de trabajo para este proyecto no está pensado para ejecutarse en múltiples hilos de ejecución, el uso de scoped_session es está pensado para el crecimiento del proyecto, y garantiza que el código se mantenga seguro, escalable y preparado para cualquier escenario de ejecución, evitando posibles errores.


### Diseño de implementación de patrones de diseño

En el apartado anterior ya pudimos ver la implementación del Singleton. Además implementé el patrón Factory, Strategy y Builder.

Teniendo en cuenta lo solicitado por la empresa: "***la empresa necesita empezar a responder preguntas clave sobre el comportamiento de ventas, por lo que deberás construir consultas SQL avanzadas que permitan transformar grandes volúmenes de datos en información clara y útil para la toma de decisiones estratégicas.***"

Comencé a diseñar informes que ofrezcan información sobre los vendedores para facilitar la visualización y el análisis de datos relevantes (por ejemplo, ventas totales por empleado, productos más vendidos, comparativas de desempeño, etc.), e información de compradores para ser implementadas a futuro.


### Patrón Factory:

**Interfaz común:**

Definimos en cada implementación un método estático `from_series(serie: pd.Series)` que recibe una fila de dataframe y devuelve una instancia de la clase creada.


```python
class BaseFactory(ABC):
    @abstractmethod
    def from_series(self, serie: pd.Series):
        pass
```

**Implementaciones concretas:**

**SalesSummary:**

```python
class SalesSummary:
    @staticmethod
    def from_series(serie: pd.Series) -> "SalesSummary":
        return SalesSummary(
            sale_id       = serie["SalesID"],
            product_id    = serie["ProductID"],
            product_name  = serie["ProductName"],
            quantity      = serie["Quantity"],
            total_price   = serie["TotalPrice"],
            customer_id   = serie["CustomerID"],
            customer_name = serie["CustomerName"],
            employee_id   = serie["EmployeeID"],
            employee_name = serie["EmployeeName"],
        )
```

Esta clase agrupa datos de las tablas `Sales`, `Products`, `Customers` y `Employees`.

**CustomerLocationInfo:**

```python
class CustomerLocationInfo:
    @staticmethod
    def from_series(serie: pd.Series) -> "CustomerLocationInfo":
        return CustomerLocationInfo(
            customer_id = serie["CustomerID"],
            full_name   = serie["CustomerName"],
            address     = serie["Address"],
            city        = serie["CityName"],
            country     = serie["CountryName"],
        )
```

Esta clase agrupa datos de las tablas `Customers` + `Cities` + `Countries` en un sólo objeto.

**Flujo de Uso:**

1. Ejecutar una consulta SQL con los campos necesarios para volcarlos a una de estas clases y transformarla en DataFrame.
2. Convertir cada fila en una clase determinada con el método `from_series`:

    ```python
    sales: List[SalesSummary] = [
        SalesSummary.from_series(row)
        for _, row in df_sales.iterrows()
    ]
    ```

3. Ya tenemos una lista de objetos SalesSummary con todos los campos renombrados y tipados, lista para:
    1. Validaciones de negocio
    2. Serialización a JSON
    3. Envío a un frontend
    4. O cualquier otra lógica sin depender del DataFrame original

**Justificación**

* Desacoplamiento: separa la lectura (SQL/CSV) de la creación de objetos de dominio.
* Reutilización: cada clase de dominio encapsula su propia lógica de mapeo.
* Flexibilidad: estas clases no están ligadas al ORM, así pueden extenderse o combinarse sin tocar las entidades de la base.
* Preparación para APIs: las clases se serializan “limpias” a JSON, exponiendo solo los campos necesarios.
* Nota: El propósito de estas clases no es persistir datos (lo hace el ORM), sino transportar datos preprocesados hacia capas de presentación, reportes o clientes externos.

**Decisión técnica:**

Esto favorece el principio abierto/cerrado (OCP), permitiendo agregar nuevas funcionalidades sin modificar el código existente, y centraliza la lógica de instanciación, lo que reduce errores y facilita el mantenimiento.


### Patrón Strategy

El patrón strategy nos permite plantear múltiples estrategias que comparten una base común y que pueden adaptarse en base a diferentes casos.

**Interfaz común**

Definimos una clase abstracta `ReportStrategy` que obliga a todas las estrategias a implementar un método único:

```python
class ReportStrategy(ABC):
    @abstractmethod
    def generate_report(self, data: pd.DataFrame, key, ascending: bool) -> pd.DataFrame:
        pass
```

**Implementaciones concretas:**

1. **TotalSalesByEmployee:**

    Esta clase genera un informe de ventas por cada vendedor, mostrando por cada uno el total de ventas
    ```python
    class TotalSalesByEmployee(ReportStrategy):
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

    ```

2. **AverageSalesByEmployee:**

    Esta clase genera un informe de ventas por vendedor, mostrando por cada uno el promedio de ventas.

    ```python
        class AverageSalesByEmployee(ReportStrategy):
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
    ```
3. **ProductSalesByEmployee:**

    Esta clase genera un informe de ventas por empleado, mostrando por cada uno la cantidad de productos vendidos.

    ```python
        class ProductSalesByEmployee(ReportStrategy):
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
    ```

**Flujo de uso**

1. **Preparar el Dataframe:** Utilizar una query que tenga las siguientes columnas:`product_id , product_name, quantity, total_price, customer_id, customer_name, employee_id, employee_name`
2. **Elegir y aplicar la estrategia:**

    ```python
        strategy = TotalSalesByEmployee()
        report_df = strategy.generate_report(
            data=df,
            key="TotalVentas",
            ascending=False
        )
        print(report_df)
    ```

**Justificación**

* Principio abierto/cerrado (OCP): Se puede agregar nuevas estrategias sin modificar las existentes
* Separación de responsabilidades: cada clase encapsula un único algoritmo de agregación y formato.
* Reutilización: el mismo constructor (ReportBuilder) y flujo puede generar tantos informes como estrategias se añadan.
* Flexibilidad: en tiempo de ejecución se elige qué tipo de análisis realizar (totales, promedios, conteos, etc.).
* Testabilidad: cada estrategia puede testearse de forma aislada, inyectando un DataFrame controlado y comprobando su salida.


### Patrón Builder

El patrón builder separa la construcción de un objeto complejo en mi caso, un conjunto de reportes y un reporte combinado de su representación, permitiendo:

* Encadenar pasos de configuración de forma legible.
* Evitar constructores con demasiados parámetros.
* Añadir nuevos pasos (por ejemplo filtros, exportación, ordenamientos) sin romper el código existente.

**Clase ReportBuilder**

La clase ReportBuilder tiene los siguientes atributos internos:

* `self.df`: El DataFrame de origen con los datos de ventas.
* `self._report_configs`: Lista de tuplas con cada estrategia de informe.
* `self.combined_sort_key` y `self.combined_sort_ascending`: Definen cómo ordenar el reporte combinado al final (por ejemplo "Nombre Apellido Vendedor").


#### Métodos encadenables

- `set_dataframe(df: pd.DataFrame)`: Establece el DataFrame base donde buscan las estrategias.
- `set_combined_sorting(key: str, ascending: bool) → self`: Configura la columna y sentido de orden para todos los reportes
- `add_report(strategy: ReportStrategy) → self`: Añade una estrategia (Strategy)
- `build_all() → Dict[str, pd.DataFrame]`: Genera todos los reportes individuales según las estrategias cargadas, y luego construye un `CombinedReport` uniendo con merge todos los resultados.
    - Este método itera en cada estrategia cargada en `_report_configs`, invocando el método `generate_report`, utilizando siempre las mismas claves de sentido y ordenamiento.

    ```python
    report = strategy.generate_report(
        self.df,
        key=self.combined_sort_key,
        ascending=self.combined_sort_ascending,
        )
    ```
    - guarda cada iteración en el diccionario de resultados, bajo el nombre de la clase de la estrategia:` result[name] = report`
    - Hace un merge progresivo de todos los elementos de result en base al id del vendedor.
    - por ultimo llama al método interno `_clean_combined_df()` para fusionar o renombrar columnas duplicadas de "Nombre Apellido Vendedor" y aplicar el ordenamiento final.
    - Devuelve un diccionario con cada reporte más el reporte combinado.

**Ejemplo de uso:**

```python
    builder = ReportBuilder()

        reports = (
            builder.set_dataframe(df_sales)
            .set_combined_sorting("EmployeeName", True)
            .add_report(TotalSalesByEmployee())
            .add_report(AverageSalesByEmployee())
            .add_report(ProductSalesByEmployee())
            .build_all()
        )
```
**Justificación**

* Construcción fluida: el cliente no necesita conocer el detalle interno de cómo se unen o limpian los reportes, sólo encadena pasos.
* Abierto/Cerrado (OCP): para agregar un nuevo tipo de reporte o un paso extra (p. ej. exportar a Excel), basta con añadir un nuevo método al builder o pasar otra estrategia, sin tocar el flujo existente.
* Separación de configuración y ejecución: primero se define qué se quiere obtener (datos, estrategias, orden), luego se ejecuta todo en build_all().
* Legibilidad: el código se lee como un pequeño “pipeline” declarativo.

> Nota: combinar Strategy con Builder permite un diseño declarativo y fluido, donde sólo cambia la configuración de estrategias para obtener distintos reportes sin tocar la lógica interna de cada una.

**Decisión de diseño**

**Elección de implementación de reportes centrados en Empleados**

Al abordar el análisis solicitado por la empresa, opté por enfocar los reportes avanzados en el desempeño de los empleados/vendedores y no en los clientes.

Esta decisión se basa en los siguientes fundamentos:

* Relevancia para la toma de decisiones: El análisis del rendimiento de los empleados es esencial para la dirección comercial, ya que permite identificar a los mejores vendedores, detectar áreas de mejora y diseñar estrategias de incentivos y capacitación.
* Mayor claridad y trazabilidad de los datos: Los datos de ventas por empleado suelen ser más robustos y estables para la comparación a lo largo del tiempo, y presentan relaciones uno-a-muchos bien definidas, lo que garantiza calidad y confiabilidad en los reportes.
* Facilidad para consultas SQL avanzadas: La estructura de la base de datos favorece la generación de métricas agregadas, rankings y comparativas por empleado, permitiendo responder rápidamente preguntas estratégicas sin ambigüedades de interpretación.
* Escalabilidad: Este enfoque no impide que en futuras iteraciones se realicen reportes por cliente, producto o cualquier otro eje; al contrario, sienta una base sólida y extensible para análisis futuros.


### Consultas desde Python

La clase de conexión expone un método para ejecutar consultas SQL simples directamente desde Python.

```python
def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la consulta: {str(e)}")

```

**Funcionamiento:**

El método recibe una cadena SQL y parámetros opcionales. Ejecuta la consulta usando SQLAlchemy. 

Los resultados se devuelven formateados como un DataFrame de Pandas. Esto facilita el análisis, visualización y procesamiento de los datos dentro del entorno Python.

**Ventajas:**

* Integración directa con todo el ecosistema de análisis de datos en Python.
* Facilidad de uso para usuarios menos experimentados (por ejemplo, analistas que no quieren lidiar con SQLAlchemy "crudo").


### Pruebas unitarias:

#### Sobre patrones de diseño:

La cobertura de pruebas unitarias se diseñó específicamente para validar el correcto funcionamiento y la integración de los patrones de diseño implementados en el sistema. 

**Prueba de Singleton**

**Objetivo:**

Asegurarse de que la clase DBConnection cumpla el patrón Singleton, es decir, que todas las instancias creadas apunten realmente al mismo objeto, compartiendo engine y sesión.

```python
def test_singleton_instance():
    db1 = DBConnection()
    db2 = DBConnection()
    assert db1 is db2
    assert db1.engine is db2.engine
    assert db1.Session is db2.Session
```

**Justificación:**

Si este test falla, existe riesgo de conexiones duplicadas o inconsistentes, lo que podría provocar errores difíciles de rastrear en sistemas más grandes.

**Pruebas de Strategy, Factory y Builder**

**a) Strategy**

Los tests de strategy se centran en comprobar que cada estrategia concreta de reporte (por ejemplo, ventas totales por empleado, promedio de ventas, productos vendidos) produce resultados correctos y coherentes según la lógica que encapsula. \
 Se valida:

* Que los reportes tengan la estructura esperada (columnas).
* Que no estén vacíos.
* Que contengan la cantidad correcta de filas según los datos de entrada.
* Que el orden de los datos sea correcto, si corresponde.

**b) Factory**

* El patrón Factory, aplicado en las clases SalesSummary y CustomerLocationInfo, centraliza y unifica la construcción de objetos complejos a partir de datos tabulares (por ejemplo, filas de un DataFrame de pandas).
* Los test verifican que el patrón Factory esté a modelos de dominio y garantizan que la construcción de objetos sea segura, homogénea 

**c) Builder**

Los tests sobre Builder buscan asegurarse de que es posible componer y encadenar estrategias para construir reportes complejos o agregados.

Se verifica:
* Que el builder puede recibir varias estrategias.
* Que los informes generados están correctamente formateados y contienen datos.
* Que los reportes combinados cumplen con los criterios de ordenamiento y formato.


#### Pruebas unitarias sobre el ORM y relaciones de entidades

Además de los tests sobre patrones de diseño, el sistema incluye un conjunto de pruebas unitarias dedicadas a verificar la correcta integración entre las clases Python y las tablas de la base de datos, así como el mapeo de relaciones (uno a muchos, muchos a uno, etc.) utilizando SQLAlchemy.

**Justificación**

Si bien la información provista y mapeada por el ORM no se utiliza en esta etapa:

* Validan que el mapeo ORM respete el modelo relacional: Al trabajar con una base de datos ya existente, es fundamental asegurarse de que cada clase refleja fielmente la tabla correspondiente y que las relaciones entre entidades (por ejemplo, cada venta tiene un cliente, producto y empleado asociados) funcionan correctamente.
* Detectan problemas de integridad y errores de configuración:
* Estos tests permiten identificar rápidamente errores en la declaración de relaciones (ForeignKey, relationship, etc.) o desincronizaciones entre el modelo Python y la base real.
* Aportan robustez a la arquitectura: Así como los patrones de diseño aseguran la escalabilidad del código, estos tests garantizan la calidad y estabilidad del acceso a datos, minimizando sorpresas a medida que el sistema crece.

**Tipos de pruebas implementadas:**

1. **Test parametrizado de consulta de entidades** (archivo test_entidades.py)
    1. Valida que cada clase modelo está correctamente enlazada con su tabla y que las consultas básicas (query.first()) funcionan sin errores.
2. **Tests de relaciones entre entidades** (archivo test_entidades.py)
    2. Clientes y su ciudad: Verifica que un cliente tenga asignada una ciudad válida.
    3. Empleados, ciudad y país: Verifica la relación encadenada empleado -> ciudad -> país.
    4. Categoría y productos: Comprueba que la relación de categoría a productos (y viceversa) existe y es funcional. 
    5. Venta y sus vínculos:Se asegura de que cada venta esté correctamente enlazada a un cliente, producto y empleado.
    6. **Valida **que las relaciones de clave foránea y los accesos por atributo funcionan correctamente en el modelo ORM.


### Seguridad de Credenciales

**1. Archivo .env**

Las credenciales de acceso a la base de datos (usuario, password, host, nombre de la base) se almacenan en un archivo .env y se accede a ellas usando la librería `python-dotenv`.

Esto evita exponer datos sensibles en el código fuente y permite una configuración flexible para diferentes entornos (desarrollo, testing, producción, etc).

**2. Protección en el repositorio**

El archivo `.env` está listado en el `.gitignore`, de modo que nunca se sube al repositorio. Así, las credenciales permanecen seguras, evitando filtraciones accidentales en plataformas públicas.

### Integración Final en Jupyter Notebook

Se incluyó un Jupyter Notebook de integración que permite:

* Verificar la conexión exitosa a la base de datos.
* Ejecutar y visualizar resultados de queries como DataFrames.
* Mostrar el uso del patrón Singleton (y cualquier otro patrón de diseño implementado).
* Ejecutar pruebas unitarias directamente desde el notebook para dejar evidencia del correcto funcionamiento.

Esto permite no solo verificar el funcionamiento de cada componente, sino también dejar evidencia replicable de todo el flujo de trabajo, facilitando tanto la evaluación académica como la adopción por otros equipos de desarrollo.


# **Tercer Avance**
## Objetivo

El sistema ya es funcional, pero ahora debes garantizar que sea eficiente y capaz de operar con agilidad frente al crecimiento del volumen de datos.
Tu desafío es optimizar las consultas y automatizar procesos clave mediante la creación de objetos avanzados en SQL.
Así, el sistema no solo será robusto, sino también estratégico: capaz de generar reportes útiles en tiempo real y facilitar decisiones informadas en la gestión del negocio.

## Entregables:

### Entregables realizados:

**Crea al menos dos queries usando**
- [x] CTE (Common Table Expressions)
- [x] Funciones ventana (ROW_NUMBER(), RANK(), etc.)
- [x] Ejecuta estas consultas desde Python (por ejemplo, con SQLAlchemy o pymysql).

**Objetos SQL**
- [x] Crea al menos dos objetos SQL, como:  Función, Trigger, Procedimiento, almacenado, Vista, Índice
- [x] Ejecútalos desde Python para demostrar su funcionamiento.

**Integración en Notebook**
- [x] Incluye todas las ejecuciones en el notebook del Avance 2.
- [x] Los resultados estén visibles.
- [x] Cada paso esté documentado con justificaciones e interpretaciones.


## Desarrollo:

### Consultas utilizando CTE y funciones ventana
#### Conocer los productos más vendidos por categoría:

```sql
    with ranked_products as (
        select c.CategoryName, p.ProductName, sum(Quantity) as total_vendido,
        dense_rank() over (
        partition by c.CategoryName
        order by sum(s.Quantity) desc 
        ) as ds
        from products p join categories c on p.CategoryID = c.CategoryID
        join sales s on s.ProductID = p.ProductID
        group by c.CategoryName, p.ProductName
        order by c.categoryName, ds)
    select * from ranked_products
    where ds<= 1
    order by categoryname, ds;
```

Esta consulta obtiene el o los productos más vendidos por cada categoría.

Se utiliza una **CTE (Common Table Expression)** para calcular el total vendido de cada producto, y se aplica la función de ventana `DENSE_RANK() `para asignar un ranking de ventas dentro de cada categoría. Finalmente, se filtran aquellos productos que ocupan el primer lugar en ventas ("estrella") en cada categoría, permitiendo detectar empates si los hubiera..

**Justificación**

Conocer el producto más vendido por categoría permite identificar cuáles son los productos clave ("estrella") en cada segmento del catálogo de productos de la empresa. Esta información es fundamental para tomar decisiones comerciales estratégicas, como focalizar acciones de marketing, gestionar el stock de manera más eficiente o identificar oportunidades para promociones específicas.

Además, permite anticipar riesgos de concentración de ventas y detectar tendencias dentro de cada categoría.

**Decisión técnica**

En este caso decidí utilizar la función ventana `dense_rank()` en vez de `row_number()` o `rank()` porque en algunos casos pueden existir empates en la cantidad máxima vendida. De esta forma, si hay dos o más productos que comparten el primer puesto dentro de una categoría, todos serán identificados como productos líderes, evitando perder información relevante sobre el desempeño de los productos.


#### Porcentaje de participación de productos en ventas

```sql
with ventas_por_categoria as (
    select
        c.CategoryID, c.CategoryName, p.ProductID, p.ProductName, SUM(s.TotalPrice) AS TotalFacturado
    from sales s
    join products p ON s.ProductID = p.ProductID
    join categories c ON p.CategoryID = c.CategoryID
    group by c.CategoryID, c.CategoryName, p.ProductID, p.ProductName
),
totales_categoria as (
    select
        CategoryID,
        SUM(TotalFacturado) AS TotalCategoria
    from ventas_por_categoria
    group by CategoryID
),
total_general_ventas as (
    select SUM(TotalFacturado) AS GranTotal from ventas_por_categoria
)
select
    v.CategoryName, v.ProductName, v.TotalFacturado, t.TotalCategoria, g.GranTotal,
    ROUND(100 * v.TotalFacturado / t.TotalCategoria, 2) AS PorcentajeEnCategoria,
    ROUND(100 * v.TotalFacturado / g.GranTotal, 2) AS PorcentajeEnTotal
from ventas_por_categoria v
join totales_categoria t ON v.CategoryID = t.CategoryID
join total_general_ventas g
order by v.CategoryName, PorcentajeEnCategoria DESC;
```


**Descripcion:**

Esta consulta calcula el total facturado por cada producto y determina su porcentaje de participación tanto dentro de su categoría como en el total general de ventas de la empresa.

Utilicé para su cálculo varias CTE para:

1. Agregar el total facturado por producto y categoría
2. Calcular el subtotal facturado por categoría
3. Obtener el total global de ventas

Luego en el select final muestro estos valores junto con el porcentaje que representa cada producto tanto en su categoría como en el total general

**Justificación**

Conocer el peso relativo de cada producto en su categoría y en el total de ventas es fundamental para la gestión estratégica de portafolios de productos.

Esta información permite:

1. Detectar productos líderes y de bajo rendimiento dentro de cada categoría.
2. Identificar riesgos de concentración excesiva de ventas en pocos productos.
3. Tomar decisiones informadas sobre inventarios, promociones, discontinuidad o refuerzo de productos.
4. Visualizar si los productos estrella de cada categoría también tienen impacto relevante en el total de la empresa, o si su importancia es solo a nivel de nicho.

**Decisión técnica**

Opté por una solución basada en CTE encadenadas para mejorar la legibilidad y modularidad del SQL.

* La CTE principal (`ventas_por_categoria`) realiza la agregación de ventas por producto y categoría.
* `totales_categoria`calcula los subtotales por categoría y permite, mediante un JOIN, relacionar cada producto con el total de su categoría para calcular su porcentaje.
* `total_general_ventas ` calcula el total global, que se incorpora a cada fila mediante un JOIN (al ser una sola fila) para que todos los productos puedan calcular su participación sobre el total de la empresa sin replicar lógica ni subconsultas en el SELECT final.


### Objetos SQL

#### Utilización de Stored Procedure para análisis de participación por producto

```sql
create procedure sp_porcentaje_producto_total(in v_cat_id int)
begin
	-- 1. ventas de todos los productos para calcular el total general
	with ventas_todas_categorias as (
		select
			c.CategoryID, c.CategoryName, p.ProductID, p.ProductName, SUM(s.TotalPrice) AS TotalFacturado
		from sales s
		join products p ON s.ProductID = p.ProductID
		join categories c ON p.CategoryID = c.CategoryID
		group by c.CategoryID, c.CategoryName, p.ProductID, p.ProductName
	),
    -- 2. filtramos las categorias que llega por parametro
    totales_por_categoria as(
		select * from ventas_todas_categorias
        where CategoryID = v_cat_id
    ),
    -- 3. calculamos los totales por la categoria
	totales_categoria as (
		select CategoryID, SUM(TotalFacturado) as TotalCategoria
        from totales_por_categoria
        group by categoryID
	),
    -- 4. calculamos el total general de ventas de todos los productos
	total_general_ventas as (
		select SUM(TotalFacturado) AS GranTotal from ventas_todas_categorias
	)
    -- usamos todo lo anterior para sacar informacion por producto
	select
		v.CategoryID, v.CategoryName, v.ProductName, v.TotalFacturado, t.TotalCategoria, g.GranTotal,
		ROUND(100 * v.TotalFacturado / t.TotalCategoria, 2) AS PorcentajeEnCategoria,
		ROUND(100 * v.TotalFacturado / g.GranTotal, 2) AS PorcentajeEnTotal
	from totales_por_categoria v
	join totales_categoria t ON v.CategoryID = t.CategoryID
	join total_general_ventas g
	order by v.CategoryName, PorcentajeEnCategoria DESC;
end
```


**Descripción**

Este procedimiento almacenado reutiliza parte de la lógica de la sección anterior en el desarrollo de “Porcentaje de participación de productos en ventas”, solamente que quise obtener el porcentaje de participación de productos pero de alguna categoría en particular.

- Tuve que rearmar la lógica para agregar el filtro que llega desde la variable de entrada `v_cat_id`.
- Por eso separo primero la ejecución del cálculo de ventas de todas las categorías, y luego uso ese resultado para filtrar.
- El cálculo que queda es bastante similar a la lógica de la CTE realizada en la sección anterior.

**Justificación**

El uso de un procedimiento almacenado permite:

* Reutilización: encapsular lógica compleja reutilizable en diferentes contextos analíticos o sistemas externos (por ejemplo, reportes automáticos o dashboards).
* Parametrización: realizar el análisis para distintas categorías de forma dinámica sin duplicar código SQL.
* Seguridad y mantenimiento: ocultar detalles internos de la lógica SQL, facilitando el mantenimiento y control de cambios desde el backend.

Además, el enfoque centrado en el análisis porcentual permite a la empresa conocer el peso relativo de cada producto en su categoría y en el total de ventas.

**Como crear el Stored Procedure desde Jupiter Notebook**

Para llamar al sp, se utilizo la clase `DBConnection` que ya teníamos, y dentro de una celda de la notebook usar los siguientes comandos: 

```python
## Stored Procedure
from sqlalchemy import text
from src.db.database import DBConnection

db = DBConnection()
engine = db.engine

create_sp_sql = """
create procedure sp_porcentaje_producto_total(in v_cat_id int)
– acá va el codigo del stored procedure
"""

with engine.begin() as conn:
    # Si ya existía, lo borramos
    conn.execute(text("DROP PROCEDURE IF EXISTS sp_porcentaje_producto_total;"))
    # Ahora creamos la nueva versión
    conn.execute(text(create_sp_sql))

print("✅ Stored procedure creado satisfactoriamente.")
```

**Para llamar al Stored Procedure**

Para llamar al sp, tuve que modificar la clase DBConnection agregando un método que me permitiera llamar stored procedures:

```python
def call_procedure(self, name: str, args: list = None) -> pd.DataFrame:
        """
        Ejecuta un stored procedure y devuelve el último result set como DataFrame.
        """
        raw = self.engine.raw_connection()
        try:
            cursor = raw.cursor()
            cursor.callproc(name, args or [])
            rows, cols = [], []
            for rs in cursor.stored_results():
                rows = rs.fetchall()
                cols = rs.column_names
            return pd.DataFrame(rows, columns=cols)
        finally:
            cursor.close()
            raw.close()
```

> 💡 Nota técnica:
>El error MySQLInterfaceError: Commands out of sync; you can't run this command now ocurre cuando se ejecuta un stored procedure y no se  consumen todos los result sets devueltos antes de cerrar la conexión.
> Por eso es fundamental consumir todos los resultados usando stored_results() y no el flujo normal de SQLAlchemy.

**Porque se produjo este error:**

Ocurre específicamente cuando se ejecuta un `CALL nombre_procedimiento(...) ` y:


* El procedimiento devuelve uno o más result sets (conjuntos de filas).
* No se consumen todos los resultados completamente antes de cerrar o reutilizar la conexión.

Cuando esto pasa, el conector queda en un estado inconsistente, ya que espera que todos los resultados hayan sido leídos antes de permitir cualquier otro comando, incluyendo el rollback() que SQLAlchemy intenta hacer automáticamente al salir del contexto with connection:.

podía llamar usando varios comandos al sp desde jupyter notebook, lo que me pareció bastante engorroso. por ello decidí agregar el método para poder ejecutar sp sin problemas.

También agregue un procedimiento para llamar vistas:

```python
def query_view(
        self, view_name: str, where: str = None, params: dict = None
    ) -> pd.DataFrame:
        """
        Hace un SELECT * desde una vista (o tabla), opcionalmente filtrando.
        """
        sql = f"SELECT * FROM {view_name}"
        if where:
            sql += f" WHERE {where}"
        # Usa execute_query para todo el trabajo
        return self.execute_query(sql, params)
```

Para separar responsabilidades.

**Uso del método**

```python
## Llamamos al stored procedure
category_id = 1  # Cambia este valor según la categoría que quieras consultar
df_porcentajes = db.call_procedure("sp_porcentaje_producto_total", [category_id])
df_porcentajes
```


### Creación de una vista

Vista: `vw_resumen_ventas_producto`:

```sql
create or replace view vw_resumen_ventas_producto AS
select
    p.ProductID,
    p.ProductName,
    c.CategoryName,
    ROUND(AVG(s.TotalPrice / NULLIF(s.Quantity, 0)), 2) AS PrecioUnitarioPromedio,
    SUM(s.Quantity) AS TotalUnidadesVendidas,
    SUM(s.TotalPrice) AS TotalFacturado,
    ROUND(SUM(s.TotalPrice) / NULLIF(SUM(s.Quantity), 0), 2) AS TicketPromedio
from sales s
join products p ON s.ProductID = p.ProductID
join categories c ON p.CategoryID = c.CategoryID
group by p.ProductID, p.ProductName, c.CategoryName
```


**Descripción**

Esta vista resume el rendimiento de cada producto en términos de ventas, brindando una perspectiva integral de su comportamiento comercial. Para cada producto muestra:

* Nombre del producto y categoría
* Precio unitario promedio (útil si hubo promociones o descuentos)
* Cantidad total vendida
* Total facturado
* Ticket promedio por unidad vendida

Esto permite identificar rápidamente productos de alto impacto, bajo rendimiento, o variaciones significativas en el precio de venta.

**Justificación**

Esta vista permite analizar rápidamente cómo se desempeña cada producto en términos de ventas, sin necesidad de escribir consultas SQL complejas cada vez.

Al centralizar esta información en una vista:

* Se ahorra tiempo para futuros análisis, ya que los datos están listos para usarse.
* Se pueden detectar productos destacados (por ventas o facturación) de forma inmediata.
* Se identifican productos con bajo rendimiento, que podrían necesitar promociones o ajustes de precio.

Ayuda a entender si los productos se venden en gran volumen pero con bajo ticket, o viceversa.

**Decisión Técnica**

La facilidad de la implementación de una vista, me llevó a elegir este tipo de estructura. Además:

* Reduce la repetición de lógica SQL compleja en análisis posteriores.
* Puede ser consumida fácilmente desde Python o herramientas de BI, sin tener que conocer la lógica interna de agregación.
* Mejora la legibilidad y modularidad del modelo de datos, separando los datos operacionales (sales, products) de las vistas analíticas.

## Optimización y análisis de rendimiento: índices

Ejemplo de índice y su impacto en el rendimiento

`CREATE INDEX idx_products_name ON products(ProductName)`;

**¿Qué hace este índice?**

Este comando crea un índice no único sobre la columna ProductName de la tabla products. El índice es una estructura (habitualmente un árbol B+) que almacena los valores de la columna ordenados y permite búsquedas rápidas.

**¿Cómo optimiza el rendimiento?**

Sin este índice, cuando se ejecuta una consulta como:

```sql
    SELECT * FROM products WHERE ProductName = 'Café molido';
```

el motor de base de datos debe recorrer toda la tabla (full table scan) para buscar coincidencias, lo cual es ineficiente si hay muchos registros.

Con el índice `idx_products_name`, MySQL puede localizar las filas deseadas de forma mucho más eficiente, consultando primero el índice y luego recuperando los datos completos. El tiempo de búsqueda disminuye considerablemente, pasando de O(n) a O(log n).

Casos en los que ayuda:

Consultas de búsqueda exacta por nombre de producto:

```sql
SELECT * FROM products WHERE ProductName = 'Café molido';
```

Consultas con comodines
```sql
SELECT * FROM products WHERE ProductName LIKE 'Caf%';
```

**Resumen:**

El índice sobre ProductName acelera de manera significativa las búsquedas, filtrados y ordenamientos que involucran esa columna, especialmente en tablas grandes.

Esto mejora el rendimiento de reportes, filtros y búsquedas en los sistemas que consumen la base de datos, brindando una mejor experiencia de usuario y menor carga sobre el servidor.


## 👩‍💻 Autor

Proyecto desarrollado por Veronica Valdez como parte del Proyecto Final del Curso Data Engineering