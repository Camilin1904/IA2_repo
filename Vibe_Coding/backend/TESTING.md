# 🧪 Guía de Testing - QuickTask API

Esta guía explica cómo ejecutar y entender las pruebas automatizadas del proyecto QuickTask.

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
2. [Estructura de Tests](#estructura-de-tests)
3. [Ejecutar Tests](#ejecutar-tests)
4. [Tipos de Tests](#tipos-de-tests)
5. [Fixtures](#fixtures)
6. [Cobertura de Código](#cobertura-de-código)
7. [Buenas Prácticas](#buenas-prácticas)

---

## 🔧 Instalación

### 1. Instalar dependencias de testing

```bash
# Instalar dependencias principales + testing
pip install -r requirements.txt
pip install -r test_requirements.txt

# O instalar todo junto
pip install -r requirements.txt -r test_requirements.txt
```

### 2. Verificar instalación

```bash
pytest --version
```

---

## 📁 Estructura de Tests

```
backend/
├── conftest.py          # Configuración global y fixtures compartidos
├── pytest.ini           # Configuración de pytest
├── test_crud.py         # Tests unitarios de operaciones CRUD
├── test_api.py          # Tests de integración de endpoints
├── test_schemas.py      # Tests de validación Pydantic
└── TESTING.md           # Esta guía
```

### Descripción de archivos

| Archivo | Descripción | Tipo |
|---------|-------------|------|
| `conftest.py` | Define fixtures globales (BD en memoria, cliente de test) | Configuración |
| `test_crud.py` | Prueba lógica de negocio (CRUD operations) | Unitario |
| `test_api.py` | Prueba endpoints HTTP completos | Integración |
| `test_schemas.py` | Prueba validación de datos con Pydantic | Unitario |

---

## ▶️ Ejecutar Tests

### Comandos básicos

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con output verboso
pytest -v

# Ejecutar tests de un archivo específico
pytest test_api.py

# Ejecutar una clase de tests específica
pytest test_api.py::TestCreateTaskEndpoint

# Ejecutar un test específico
pytest test_api.py::TestCreateTaskEndpoint::test_create_task_success

# Ejecutar tests que coincidan con un patrón
pytest -k "create"

# Detener en el primer error
pytest -x

# Mostrar prints durante los tests
pytest -s
```

### Ejecutar por categoría

```bash
# Solo tests unitarios
pytest test_crud.py test_schemas.py

# Solo tests de integración
pytest test_api.py

# Tests relacionados con creación
pytest -k "create"

# Tests relacionados con actualización
pytest -k "update"
```

---

## 🔍 Tipos de Tests

### 1. Tests Unitarios (`test_crud.py`)

Prueban la **lógica de negocio** de forma aislada.

**Ejemplo:**
```python
def test_create_task_minimal(test_db):
    """Crear tarea solo con título"""
    task_data = TaskCreate(title="Llamar al médico")
    task = crud.create_task(test_db, task_data)
    
    assert task.id is not None
    assert task.title == "Llamar al médico"
```

**Cobertura:**
- ✅ Crear tareas (completas y mínimas)
- ✅ Leer tareas (por ID, todas, con filtros)
- ✅ Actualizar tareas (parcial y completa)
- ✅ Eliminar tareas
- ✅ Búsqueda y filtrado
- ✅ Paginación

### 2. Tests de Integración (`test_api.py`)

Prueban **endpoints HTTP completos** (request → response).

**Ejemplo:**
```python
def test_create_task_success(client):
    """Crear tarea vía POST /tasks"""
    response = client.post("/tasks", json={
        "title": "Nueva tarea",
        "completed": False
    })
    
    assert response.status_code == 201
    assert response.json()["title"] == "Nueva tarea"
```

**Cobertura:**
- ✅ GET `/tasks` (listar con filtros)
- ✅ GET `/tasks/{id}` (obtener por ID)
- ✅ POST `/tasks` (crear)
- ✅ PUT `/tasks/{id}` (actualizar completa)
- ✅ PATCH `/tasks/{id}` (actualizar parcial)
- ✅ DELETE `/tasks/{id}` (eliminar)
- ✅ Casos de error (404, 422)
- ✅ Flujos completos (E2E)

### 3. Tests de Validación (`test_schemas.py`)

Prueban **validación de datos con Pydantic**.

**Ejemplo:**
```python
def test_empty_title_raises_error():
    """Título vacío debe fallar"""
    with pytest.raises(ValidationError):
        TaskCreate(title="")
```

**Cobertura:**
- ✅ Campos obligatorios
- ✅ Límites de longitud
- ✅ Tipos de datos
- ✅ Valores por defecto

---

## 🎯 Fixtures

Los **fixtures** son funciones reutilizables que preparan el entorno de test.

### Fixtures disponibles (en `conftest.py`)

#### 1. `test_db`
Proporciona una **base de datos SQLite en memoria**.

```python
def test_example(test_db):
    # test_db es una sesión de BD temporal
    task = crud.create_task(test_db, TaskCreate(title="Test"))
    assert task.id is not None
```

**Características:**
- Se crea nueva para cada test (aislamiento)
- Se destruye automáticamente después del test
- No persiste datos entre tests

#### 2. `client`
Proporciona un **cliente de prueba de FastAPI**.

```python
def test_example(client):
    # client simula peticiones HTTP
    response = client.get("/tasks")
    assert response.status_code == 200
```

**Características:**
- Usa la BD en memoria automáticamente
- No hace peticiones HTTP reales
- Más rápido que peticiones reales

#### 3. `sample_task_data`
Proporciona **datos de ejemplo** para crear tareas.

```python
def test_example(sample_task_data):
    # sample_task_data es un diccionario con datos válidos
    assert sample_task_data["title"] == "Tarea de prueba"
```

#### 4. `create_sample_task`
Crea una **tarea de ejemplo** y retorna la respuesta.

```python
def test_example(create_sample_task):
    # create_sample_task ya existe en la BD
    task_id = create_sample_task["id"]
    # Ahora puedes usarla para tests de actualización/eliminación
```

---

## 📊 Cobertura de Código

### Ejecutar con reporte de cobertura

```bash
# Generar reporte de cobertura
pytest --cov=. --cov-report=html

# Ver reporte en terminal
pytest --cov=. --cov-report=term-missing

# Solo mostrar archivos con menos del 100%
pytest --cov=. --cov-report=term-missing:skip-covered
```

### Ver reporte HTML

```bash
# Generar y abrir en navegador
pytest --cov=. --cov-report=html
open htmlcov/index.html  # En Mac/Linux
# start htmlcov/index.html  # En Windows
```

### Interpretar resultados

```
Name           Stmts   Miss  Cover
----------------------------------
main.py           45      2    96%
crud.py           38      0   100%
models.py         12      0   100%
schemas.py        25      1    96%
----------------------------------
TOTAL            120      3    98%
```

- **Stmts**: Líneas de código
- **Miss**: Líneas no ejecutadas
- **Cover**: Porcentaje de cobertura

---

## ✅ Buenas Prácticas

### 1. Nomenclatura de tests

```python
# ✅ Bueno - Describe claramente qué se prueba
def test_create_task_with_all_fields():
    pass

def test_update_task_title_only():
    pass

# ❌ Malo - Nombre poco descriptivo
def test_task1():
    pass

def test_update():
    pass
```

### 2. Organización con clases

```python
class TestCreateTask:
    """Agrupa todos los tests de creación"""
    
    def test_create_success(self):
        pass
    
    def test_create_without_title(self):
        pass
```

### 3. Assertions claras

```python
# ✅ Bueno - Assertion específica
assert response.status_code == 201
assert task.title == "Nueva tarea"

# ❌ Malo - Assertion genérica
assert response
assert task
```

### 4. Arrange-Act-Assert (AAA)

```python
def test_create_task():
    # Arrange (preparar)
    task_data = TaskCreate(title="Test")
    
    # Act (ejecutar)
    task = crud.create_task(db, task_data)
    
    # Assert (verificar)
    assert task.id is not None
```

### 5. Tests independientes

```python
# ✅ Bueno - Cada test crea sus datos
def test_a(client):
    task = client.post("/tasks", json={"title": "Tarea A"})
    assert task.status_code == 201

def test_b(client):
    task = client.post("/tasks", json={"title": "Tarea B"})
    assert task.status_code == 201

# ❌ Malo - test_b depende de test_a
def test_a(client):
    global task_id
    task = client.post("/tasks", json={"title": "Tarea"})
    task_id = task.json()["id"]

def test_b(client):
    # Asume que test_a ya corrió
    response = client.get(f"/tasks/{task_id}")
```

---

## 📝 Ejemplos de Uso

### Caso 1: Probar solo la creación

```bash
pytest -k "create" -v
```

### Caso 2: Probar endpoint específico

```bash
pytest test_api.py::TestCreateTaskEndpoint -v
```

### Caso 3: Debug de un test que falla

```bash
# Ver más detalles del error
pytest test_api.py::TestCreateTaskEndpoint::test_create_task_success -vv

# Ver prints
pytest test_api.py::TestCreateTaskEndpoint::test_create_task_success -s
```

### Caso 4: Ejecutar tests rápidos

```bash
# Omitir tests marcados como lentos
pytest -m "not slow"
```

---

## 🐛 Troubleshooting

### Error: "No module named 'fastapi'"

```bash
# Instalar dependencias
pip install -r requirements.txt -r test_requirements.txt
```

### Error: "database is locked"

Asegúrate de usar `sqlite:///:memory:` en tests (ya está configurado en `conftest.py`).

### Tests pasan individualmente pero fallan juntos

Verifica que los tests sean independientes (no compartan estado).

---

## 📚 Recursos Adicionales

- [Documentación pytest](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

---

## 📊 Resumen de Cobertura Actual

| Componente | Tests | Cobertura Estimada |
|------------|-------|-------------------|
| CRUD Operations | 21 tests | ~95% |
| API Endpoints | 25 tests | ~90% |
| Schemas | 11 tests | ~85% |
| **TOTAL** | **57 tests** | **~90%** |

---

**¡Happy Testing!** 🚀✅
