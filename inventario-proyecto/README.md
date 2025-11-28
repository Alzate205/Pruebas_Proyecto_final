# Sistema de Gestión de Inventario

Sistema completo de gestión de inventario con API REST, interfaz web y pruebas automatizadas.

## Descripción del Proyecto

Este proyecto es un sistema de gestión de inventario que permite administrar productos y categorías. Incluye:
- API REST desarrollada con FastAPI
- Interfaz web con HTML/CSS/JavaScript
- Base de datos SQLite con SQLAlchemy
- Suite completa de pruebas (unitarias, integración, E2E)
- Pipeline de CI/CD con GitHub Actions
- Análisis estático de código con Flake8

## Arquitectura

### Backend
El backend sigue una arquitectura por capas:
```
backend/
├── app/
│   ├── api/           # Controladores (endpoints)
│   ├── models.py      # Modelos de base de datos
│   ├── schemas.py     # Esquemas Pydantic
│   ├── crud.py        # Lógica de negocio
│   ├── database.py    # Configuración de BD
│   └── tests/         # Pruebas automatizadas
```

**Capas**:
1. **API (Controladores)**: Endpoints REST que reciben requests HTTP
2. **Servicios (CRUD)**: Lógica de negocio y validaciones
3. **Modelos**: Definición de tablas de base de datos
4. **Schemas**: Validación y serialización de datos

### Base de Datos

**Tabla: categories**
- id: Integer (PK)
- name: String (único, no nulo)

**Tabla: products**
- id: Integer (PK)
- name: String (no nulo)
- description: String (no nulo)
- price: Float (no nulo)
- stock: Integer (no nulo)
- category_id: Integer (FK a categories.id, no nulo)

**Relación**: Una categoría tiene muchos productos (1:N)

## Instalación

### Prerrequisitos
- Python 3.11+
- pip
- Git

### Paso 1: Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd inventario-proyecto
```

### Paso 2: Instalar dependencias del backend
```bash
cd backend
pip install -r requirements.txt
```

### Paso 3: Instalar navegadores para pruebas E2E
```bash
playwright install
```

## Ejecución

### Ejecutar el Backend (API)
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000
Documentación Swagger: http://localhost:8000/docs

### Ejecutar el Frontend
En otra terminal:
```bash
cd frontend
python -m http.server 3000
```

La interfaz estará disponible en: http://localhost:3000

## Pruebas

### Ejecutar todas las pruebas
```bash
cd backend
pytest -v
```

### Ejecutar pruebas por tipo

**Pruebas unitarias**:
```bash
pytest app/tests/unit -v
```

**Pruebas de integración**:
```bash
pytest app/tests/integration -v
```

**Pruebas E2E** (requiere backend y frontend ejecutándose):
```bash
pytest app/tests/e2e -v
```

### Análisis estático
```bash
cd backend
flake8 app
```

## Endpoints de la API

### Categorías
- `POST /api/categories/` - Crear categoría
- `GET /api/categories/` - Listar categorías

### Productos
- `POST /api/products/` - Crear producto
- `GET /api/products/` - Listar productos
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

## Pipeline de CI/CD

El proyecto incluye un workflow de GitHub Actions que:

1. Instala dependencias
2. Ejecuta análisis estático (Flake8)
3. Ejecuta pruebas unitarias
4. Ejecuta pruebas de integración
5. Ejecuta pruebas E2E
6. Si todo pasa, imprime "OK"

Ver configuración en: `.github/workflows/ci.yml`

## Decisiones Técnicas

### FastAPI
Elegido por su rendimiento, validación automática con Pydantic y documentación automática.

### SQLite
Base de datos ligera ideal para desarrollo y demostración. Fácil migración a PostgreSQL/MySQL.

### Playwright
Framework moderno para pruebas E2E, más robusto que Selenium.

### Arquitectura por capas
Separación clara de responsabilidades: API, lógica de negocio, acceso a datos.

### GitHub Actions
CI/CD integrado con GitHub, configuración simple y efectiva.

## Uso de la Aplicación

### Crear Categoría
1. En la sección "Crear Categoría", ingresa un nombre
2. Haz clic en "Crear Categoría"
3. La categoría aparecerá en la tabla

### Crear Producto
1. Primero crea al menos una categoría
2. Llena el formulario de producto con todos los campos
3. Selecciona una categoría
4. Haz clic en "Crear Producto"

### Editar Producto
1. En la tabla de productos, haz clic en "Editar"
2. Modifica los campos necesarios
3. Haz clic en "Actualizar Producto"

### Eliminar Producto
1. En la tabla de productos, haz clic en "Eliminar"
2. Confirma la acción

## Ejecución con Docker (Opcional)

### Crear Dockerfile para backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Construir y ejecutar
```bash
docker build -t inventory-api ./backend
docker run -p 8000:8000 inventory-api
```

## Estructura del Proyecto
```
inventario-proyecto/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── categories.py
│   │   │   └── products.py
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── .flake8
├── frontend/
│   ├── index.html
│   └── app.js
├── .github/
│   └── workflows/
│       └── ci.yml
├── PLAN_DE_PRUEBAS.md
├── pytest.ini
└── README.md
```

## Autor
Estudiante de Ingeniería de Software
Asignatura: Pruebas de Software

## Licencia
MIT