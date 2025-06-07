# Proyecto Final - Data Engineering

---

## 🛠️ ¿Qué se hizo?

- 📄 **Modelado relacional en MySQL**:  
  Se creó una base de datos llamada `sales_company` con tablas normalizadas y claves primarias, respetando la integridad referencial del negocio.

- 📥 **Carga de datos desde archivos `.csv`**:  
  Se implementó un script `load_data.sql` que crea las tablas y carga los datos con `LOAD DATA LOCAL INFILE` desde rutas absolutas.

- 🧱 **Programación Orientada a Objetos (POO)**:  
  Se desarrolló una clase en Python por cada tabla (`Product`, `Customer`, `Sale`, etc.) aplicando:
  - Encapsulamiento
  - Constructores personalizados
  - Métodos específicos de negocio (ej: aplicar descuentos, calcular precios finales, validar datos)

- ✅ **Pruebas unitarias con `pytest`**:  
  Se implementaron pruebas sobre métodos clave, como `apply_discount()` y validaciones de entrada (`ValueError`), asegurando la calidad del comportamiento.

---

## 📁 Estructura del Proyecto

```css
proyecto_final/
├── data/ # Archivos CSV originales
├── sql/
│ └── load_data.sql # Script SQL para crear base y cargar datos
├── src/
│ └── models/ # Clases POO por entidad
│ ├── product.py
│ ├── customer.py
│ └── ...
├── tests/
│ └── test_product.py # Pruebas automatizadas con pytest
├── main.py # Punto de entrada para pruebas y lógica futura
└── README.md # Documentación del proyecto

```


---

## 💡 Justificación técnica

- Se utilizó **MySQL** como base de datos relacional, soporte de carga masiva de datos, y compatibilidad con herramientas del ecosistema.
- La carga de datos se realizó mediante `LOAD DATA LOCAL INFILE`, priorizando eficiencia en comparación con inserciones fila por fila.
- Las clases en Python están diseñadas bajo **principios de POO** para permitir la reutilización, validación de datos, y crecimiento futuro del sistema.
- `pytest` fue elegido como framework de testing por su simplicidad, velocidad y facilidad de integración con proyectos en Python moderno.

---

## 🚧 Próximos pasos

- Implementar carga y validación automática desde `.csv` con `pandas`.
- Conexión a base de datos desde Python (`MySQL Connector` o `SQLAlchemy`).
- Análisis de datos, dashboards y generación de reportes.
- Integración con API REST para carga y consulta de datos.

---

## 👩‍💻 Autor

Proyecto desarrollado por Veronica Valdez como parte del Proyecto Final del Curso Data Engineering
