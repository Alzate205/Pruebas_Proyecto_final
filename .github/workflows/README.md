# GitHub Actions CI/CD Pipeline

Este directorio contiene los workflows de GitHub Actions para ejecutar tests automáticamente.

## Workflows disponibles

### `tests.yml` - Pipeline de Tests

Este workflow ejecuta automáticamente todos los tests del proyecto.

#### Cuándo se ejecuta

- **Push** a las ramas `main` o `develop`
- **Pull Requests** hacia `main` o `develop`
- **Manualmente** desde la pestaña "Actions" en GitHub

#### Jobs

##### 1. Unit and Integration Tests
- Ejecuta tests unitarios (`app/tests/unit/`)
- Ejecuta tests de integración (`app/tests/integration/`)
- Usa Python 3.11
- Plataforma: Ubuntu latest

##### 2. E2E Tests
- Ejecuta tests end-to-end (`app/tests/e2e/`)
- Instala Playwright y navegadores
- Usa Python 3.11
- Plataforma: Ubuntu latest

#### Requisitos

El workflow requiere que:
- Exista `inventario-proyecto/backend/requirements.txt` con todas las dependencias
- Los tests estén en `inventario-proyecto/backend/app/tests/`
- El archivo `pytest.ini` esté configurado correctamente

#### Ver resultados

1. Ve a la pestaña **Actions** en tu repositorio de GitHub
2. Selecciona el workflow "Tests"
3. Haz clic en cualquier ejecución para ver los detalles
4. Los artefactos (logs, base de datos) se guardan por 7 días en caso de fallos

## Ejecutar tests localmente

Para ejecutar los mismos tests que el pipeline:

```bash
# Navegar al directorio backend
cd inventario-proyecto/backend

# Tests unitarios
python -m pytest app/tests/unit/ -v

# Tests de integración
python -m pytest app/tests/integration/ -v

# Tests E2E
python -m pytest app/tests/e2e/ -v

# Todos los tests
python -m pytest -v
```

## Badges

Puedes agregar un badge al README principal:

```markdown
![Tests](https://github.com/TU-USUARIO/TU-REPO/workflows/Tests/badge.svg)
```
