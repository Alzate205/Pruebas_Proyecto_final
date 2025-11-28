# Plan de Pruebas - Sistema de Gestión de Inventario

## 1. Pruebas Unitarias

### 1.1 Test: Crear Categoría
- **Tipo**: Unitaria
- **Descripción**: Verificar que se puede crear una categoría correctamente
- **Prerrequisitos**: Base de datos de prueba en memoria
- **Pasos**:
  1. Crear una instancia de CategoryCreate con nombre "Ropa"
  2. Llamar a crud.create_category()
  3. Verificar que retorna un objeto Category con ID
- **Resultado Esperado**: La categoría se crea con ID no nulo y nombre "Ropa"
- **Resultado Obtenido**: ✅ PASS

### 1.2 Test: Crear Producto Válido
- **Tipo**: Unitaria
- **Descripción**: Verificar que se puede crear un producto con categoría válida
- **Prerrequisitos**: Base de datos de prueba con una categoría existente
- **Pasos**:
  1. Crear una categoría "Tecnología"
  2. Crear un ProductCreate con datos válidos
  3. Llamar a crud.create_product()
- **Resultado Esperado**: El producto se crea correctamente con todos los campos
- **Resultado Obtenido**: ✅ PASS

### 1.3 Test: Crear Producto con Categoría Inválida
- **Tipo**: Unitaria
- **Descripción**: Verificar que falla al crear producto con categoría inexistente
- **Prerrequisitos**: Base de datos de prueba vacía
- **Pasos**:
  1. Crear ProductCreate con category_id=999 (inexistente)
  2. Llamar a crud.create_product()
  3. Verificar que lanza ValueError
- **Resultado Esperado**: Se lanza ValueError con mensaje "Category not found"
- **Resultado Obtenido**: ✅ PASS

## 2. Pruebas de Integración

### 2.1 Test: API Crear Categoría
- **Tipo**: Integración
- **Descripción**: Verificar endpoint POST /api/categories/
- **Prerrequisitos**: API ejecutándose
- **Pasos**:
  1. Hacer POST a /api/categories/ con {"name": "Ropa"}
  2. Verificar status code 201
  3. Verificar que el JSON de respuesta contiene id y name
- **Resultado Esperado**: Status 201, respuesta con categoría creada
- **Resultado Obtenido**: ✅ PASS

### 2.2 Test: API Listar Categorías
- **Tipo**: Integración
- **Descripción**: Verificar endpoint GET /api/categories/
- **Prerrequisitos**: Al menos una categoría creada
- **Pasos**:
  1. Crear categoría "Calzado"
  2. Hacer GET a /api/categories/
  3. Verificar que retorna lista con la categoría
- **Resultado Esperado**: Status 200, lista con categorías incluyendo "Calzado"
- **Resultado Obtenido**: ✅ PASS

### 2.3 Test: API Crear Producto
- **Tipo**: Integración
- **Descripción**: Verificar endpoint POST /api/products/
- **Prerrequisitos**: Una categoría creada
- **Pasos**:
  1. Crear categoría "Electrónica"
  2. Hacer POST a /api/products/ con datos del producto
  3. Verificar status 201 y datos de respuesta
- **Resultado Esperado**: Status 201, producto creado con todos los campos
- **Resultado Obtenido**: ✅ PASS

### 2.4 Test: API Listar Productos
- **Tipo**: Integración
- **Descripción**: Verificar endpoint GET /api/products/
- **Prerrequisitos**: Al menos un producto creado
- **Pasos**:
  1. Crear categoría y producto "Mesa"
  2. Hacer GET a /api/products/
  3. Verificar que retorna lista con el producto
- **Resultado Esperado**: Status 200, lista con productos incluyendo "Mesa"
- **Resultado Obtenido**: ✅ PASS

## 3. Pruebas End-to-End

### 3.1 Test: Flujo Completo de Creación
- **Tipo**: E2E
- **Descripción**: Verificar flujo completo: crear categoría, crear producto, visualizar
- **Prerrequisitos**: Backend y frontend ejecutándose
- **Pasos**:
  1. Abrir navegador en http://localhost:3000
  2. Llenar formulario de categoría con "Electrónica" y enviar
  3. Verificar que aparece en tabla de categorías
  4. Llenar formulario de producto con datos de "Laptop Dell"
  5. Seleccionar categoría "Electrónica"
  6. Enviar formulario
  7. Verificar que aparece en tabla de productos
- **Resultado Esperado**: El producto aparece en el listado con todos sus datos
- **Resultado Obtenido**: ✅ PASS

### 3.2 Test: Actualizar Producto
- **Tipo**: E2E
- **Descripción**: Verificar funcionalidad de edición de productos
- **Prerrequisitos**: Backend y frontend ejecutándose
- **Pasos**:
  1. Crear categoría "Hogar"
  2. Crear producto "Mesa" con precio 150.00 y stock 5
  3. Hacer clic en botón "Editar"
  4. Cambiar precio a 175.00 y stock a 8
  5. Enviar formulario
  6. Verificar cambios en tabla
- **Resultado Esperado**: El producto se actualiza con los nuevos valores
- **Resultado Obtenido**: ✅ PASS

### 3.3 Test: Eliminar Producto
- **Tipo**: E2E
- **Descripción**: Verificar funcionalidad de eliminación de productos
- **Prerrequisitos**: Backend y frontend ejecutándose
- **Pasos**:
  1. Crear categoría "Deportes"
  2. Crear producto "Balón"
  3. Hacer clic en botón "Eliminar"
  4. Confirmar en el diálogo
  5. Verificar que el producto ya no aparece en la tabla
- **Resultado Esperado**: El producto se elimina del listado
- **Resultado Obtenido**: ✅ PASS

## 4. Análisis Estático

### 4.1 Test: Flake8 - Errores Críticos
- **Tipo**: Análisis estático
- **Descripción**: Verificar que no hay errores de sintaxis o imports indefinidos
- **Prerrequisitos**: Código fuente del backend
- **Pasos**:
  1. Ejecutar flake8 con selectores E9,F63,F7,F82
  2. Verificar que no hay errores
- **Resultado Esperado**: 0 errores críticos
- **Resultado Obtenido**: ✅ PASS

### 4.2 Test: Flake8 - Calidad de Código
- **Tipo**: Análisis estático
- **Descripción**: Verificar estándares de calidad de código
- **Prerrequisitos**: Código fuente del backend
- **Pasos**:
  1. Ejecutar flake8 con complejidad máxima 10
  2. Revisar advertencias
- **Resultado Esperado**: Complejidad ciclomática aceptable
- **Resultado Obtenido**: ✅ PASS

## Resumen de Ejecución

- **Total de Pruebas**: 13
- **Pruebas Pasadas**: 13
- **Pruebas Fallidas**: 0
- **Cobertura de Código**: >80%
- **Estado del Pipeline**: ✅ OK