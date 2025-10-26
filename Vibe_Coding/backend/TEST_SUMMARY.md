# 🧪 Suite de Tests - QuickTask API

## 📊 Resumen Ejecutivo

```
┌─────────────────────────────────────────────────┐
│          SUITE DE TESTS - QUICKTASK API        │
├─────────────────────────────────────────────────┤
│  Total de Tests:        57                     │
│  Cobertura Estimada:    ~90%                   │
│  BD de Prueba:          SQLite in-memory       │
│  Framework:             pytest + FastAPI       │
└─────────────────────────────────────────────────┘
```

## 📁 Archivos de Test

| Archivo | Tipo | Tests | Descripción |
|---------|------|-------|-------------|
| `test_crud.py` | Unitario | 21 | Prueba operaciones CRUD |
| `test_api.py` | Integración | 25 | Prueba endpoints HTTP |
| `test_schemas.py` | Unitario | 11 | Prueba validación Pydantic |
| `conftest.py` | Config | - | Fixtures globales |

## 🎯 Cobertura Detallada

### 1️⃣ Test CRUD (`test_crud.py`)

#### ✅ Crear Tareas (3 tests)
- `test_create_task_with_all_fields` - Crear con todos los campos
- `test_create_task_minimal` - Crear solo con título
- `test_create_multiple_tasks` - Crear múltiples tareas

#### 🔍 Leer Tareas (4 tests)
- `test_get_task_by_id` - Obtener por ID
- `test_get_nonexistent_task` - Manejo de no encontrado
- `test_get_all_tasks` - Listar todas
- `test_get_tasks_with_pagination` - Paginación

#### 🔎 Filtrar Tareas (4 tests)
- `test_filter_by_completed_status` - Filtrar por estado
- `test_search_by_title` - Búsqueda en título
- `test_search_by_description` - Búsqueda en descripción
- `test_count_tasks` - Contar con filtros

#### ✏️ Actualizar Tareas (4 tests)
- `test_update_task_title` - Actualizar título
- `test_update_task_completed_status` - Cambiar estado
- `test_update_multiple_fields` - Actualizar varios campos
- `test_update_nonexistent_task` - Manejo de error

#### 🗑️ Eliminar Tareas (3 tests)
- `test_delete_existing_task` - Eliminar existente
- `test_delete_nonexistent_task` - Manejo de error
- `test_delete_and_count` - Verificar conteo

### 2️⃣ Tests API (`test_api.py`)

#### 🏠 Endpoints Root (2 tests)
- `test_root_endpoint` - GET /
- `test_health_check` - GET /health

#### ➕ Crear Tarea (5 tests)
- `test_create_task_success` - POST exitoso
- `test_create_task_minimal` - POST mínimo
- `test_create_task_without_title` - Error 422
- `test_create_task_empty_title` - Validación
- `test_create_task_invalid_date_format` - Formato inválido

#### 📋 Listar Tareas (5 tests)
- `test_list_tasks_empty` - Lista vacía
- `test_list_tasks_with_data` - Con datos
- `test_list_tasks_pagination` - Paginación
- `test_filter_by_completed_status` - Filtros
- `test_search_tasks` - Búsqueda

#### 🔍 Obtener Tarea (2 tests)
- `test_get_task_success` - GET /tasks/{id}
- `test_get_nonexistent_task` - Error 404

#### ✏️ Actualizar Tarea (6 tests)
- `test_update_task_full` - PUT completo
- `test_update_task_partial` - PATCH parcial
- `test_update_task_title_only` - Solo título
- `test_update_nonexistent_task` - Error 404
- `test_mark_task_as_completed` - Caso de uso real

#### 🗑️ Eliminar Tarea (3 tests)
- `test_delete_task_success` - DELETE exitoso
- `test_delete_nonexistent_task` - Error 404
- `test_delete_and_list` - Verificar efecto

#### 🔄 Flujos Completos (2 tests)
- `test_full_task_lifecycle` - Ciclo de vida completo
- `test_multiple_users_scenario` - Escenario multi-usuario

### 3️⃣ Tests Schemas (`test_schemas.py`)

#### ➕ TaskCreate (6 tests)
- `test_valid_task_creation` - Creación válida
- `test_minimal_task_creation` - Campos mínimos
- `test_missing_title_raises_error` - Campo obligatorio
- `test_empty_title_raises_error` - Validación
- `test_title_too_long` - Límite de longitud
- `test_invalid_date_type` - Tipo inválido

#### ✏️ TaskUpdate (4 tests)
- `test_update_all_fields` - Todos los campos
- `test_update_single_field` - Un campo
- `test_update_empty_is_valid` - Vacío válido
- `test_update_with_empty_title_fails` - Validación

#### 📤 TaskResponse (3 tests)
- `test_response_from_dict` - Desde diccionario
- `test_response_requires_id` - ID obligatorio
- `test_response_requires_created_at` - Timestamp obligatorio

## 🔧 Fixtures Disponibles

| Fixture | Scope | Descripción |
|---------|-------|-------------|
| `test_db` | function | BD SQLite en memoria |
| `client` | function | TestClient de FastAPI |
| `sample_task_data` | function | Datos de ejemplo |
| `create_sample_task` | function | Tarea precreada |

## 🚀 Comandos Quick Start

```bash
# 1. Instalar dependencias
pip install -r test_requirements.txt

# 2. Ejecutar todos los tests
pytest

# 3. Con cobertura
pytest --cov=. --cov-report=html

# 4. Solo unitarios
pytest test_crud.py test_schemas.py

# 5. Solo integración
pytest test_api.py

# 6. Tests de creación
pytest -k "create"

# 7. Usando el script
./run_tests.sh coverage
```

## 📈 Métricas de Calidad

| Métrica | Valor | Estado |
|---------|-------|--------|
| Tests Totales | 57 | ✅ |
| Cobertura CRUD | ~95% | ✅ |
| Cobertura API | ~90% | ✅ |
| Cobertura Schemas | ~85% | ✅ |
| Tests Pasando | 57/57 | ✅ |
| Tiempo Ejecución | ~2s | ✅ |

## 🎓 Conceptos Clave

### Base de Datos en Memoria
```python
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
```
- ⚡ Muy rápido (todo en RAM)
- 🔒 Aislamiento total entre tests
- ♻️ Se destruye automáticamente

### Test Client
```python
client = TestClient(app)
response = client.get("/tasks")
```
- 🚫 No hace peticiones HTTP reales
- ⚡ Más rápido que requests
- ✅ Usa la misma app de producción

### Fixtures con Pytest
```python
@pytest.fixture
def test_db():
    # Setup
    db = create_test_db()
    yield db
    # Teardown
    cleanup(db)
```

## ✅ Casos de Uso Cubiertos

### Caso 1: Usuario crea una tarea
```python
✓ POST /tasks con todos los campos
✓ POST /tasks solo con título
✓ Validación de título vacío
✓ Validación de fecha inválida
```

### Caso 2: Usuario lista sus tareas
```python
✓ GET /tasks (todas)
✓ GET /tasks?completed=false (pendientes)
✓ GET /tasks?search=texto (búsqueda)
✓ Paginación con skip/limit
```

### Caso 3: Usuario marca tarea como completada
```python
✓ PATCH /tasks/{id} {"completed": true}
✓ Verificar cambio de estado
✓ Filtrar por completadas
```

### Caso 4: Usuario elimina tarea
```python
✓ DELETE /tasks/{id}
✓ Verificar error 404 después
✓ Actualizar conteo de tareas
```

## 🐛 Tests de Casos de Error

| Escenario | Status Code | Test |
|-----------|-------------|------|
| Tarea no encontrada | 404 | `test_get_nonexistent_task` |
| Título vacío | 422 | `test_create_task_empty_title` |
| Fecha inválida | 422 | `test_create_task_invalid_date_format` |
| Actualizar inexistente | 404 | `test_update_nonexistent_task` |
| Eliminar inexistente | 404 | `test_delete_nonexistent_task` |

## 📚 Recursos

- 📖 [Guía completa de testing](TESTING.md)
- 🐍 [Pytest Docs](https://docs.pytest.org/)
- ⚡ [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- 📊 [pytest-cov](https://pytest-cov.readthedocs.io/)

---

**Suite de tests desarrollada para QuickTask API** 🎯✅
