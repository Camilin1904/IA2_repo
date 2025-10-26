# 🚀 Quick Start - Testing QuickTask API

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar
```bash
cd backend
pip install -r requirements.txt -r test_requirements.txt
```

### 2️⃣ Ejecutar
```bash
pytest -v
```

### 3️⃣ Ver Cobertura
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## 📸 Ejemplos de Ejecución

### Ejemplo 1: Todos los tests
```bash
$ pytest

======================== test session starts =========================
collected 57 items

test_crud.py::TestCreateTask::test_create_task_with_all_fields PASSED [ 1%]
test_crud.py::TestCreateTask::test_create_task_minimal PASSED        [ 3%]
test_api.py::TestCreateTaskEndpoint::test_create_task_success PASSED [ 5%]
...

===================== 57 passed in 2.34s ============================
```

### Ejemplo 2: Solo tests de creación
```bash
$ pytest -k "create" -v

======================== test session starts =========================
test_crud.py::TestCreateTask::test_create_task_with_all_fields PASSED
test_crud.py::TestCreateTask::test_create_task_minimal PASSED
test_crud.py::TestCreateTask::test_create_multiple_tasks PASSED
test_api.py::TestCreateTaskEndpoint::test_create_task_success PASSED
test_api.py::TestCreateTaskEndpoint::test_create_task_minimal PASSED
test_api.py::TestCreateTaskEndpoint::test_create_task_without_title PASSED
test_api.py::TestCreateTaskEndpoint::test_create_task_empty_title PASSED
test_schemas.py::TestTaskCreateSchema::test_valid_task_creation PASSED

===================== 8 passed in 0.45s =============================
```

### Ejemplo 3: Con reporte de cobertura
```bash
$ pytest --cov=. --cov-report=term-missing

======================== test session starts =========================
collected 57 items

test_crud.py ........................                                [ 42%]
test_api.py ............................                             [ 91%]
test_schemas.py .....                                                [100%]

---------- coverage: platform linux, python 3.10.12 -----------
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
main.py            45      2    96%   158-159
crud.py            38      0   100%
models.py          12      0   100%
schemas.py         25      1    96%   42
database.py        15      0   100%
---------------------------------------------
TOTAL             135      3    98%

===================== 57 passed in 2.34s ============================
```

---

## 🎯 Casos de Uso Comunes

### ✅ Test un endpoint específico
```bash
pytest test_api.py::TestCreateTaskEndpoint::test_create_task_success -v
```

### ✅ Test una clase completa
```bash
pytest test_api.py::TestCreateTaskEndpoint -v
```

### ✅ Solo tests unitarios
```bash
pytest test_crud.py test_schemas.py -v
```

### ✅ Solo tests de integración
```bash
pytest test_api.py -v
```

### ✅ Detener en el primer error
```bash
pytest -x
```

### ✅ Ver prints durante tests
```bash
pytest -s
```

### ✅ Modo silencioso
```bash
pytest -q
```

---

## 🛠️ Usar el Script Helper

```bash
# Dar permisos (solo la primera vez)
chmod +x run_tests.sh

# Ejecutar todos los tests
./run_tests.sh

# Solo tests unitarios
./run_tests.sh unit

# Solo tests de integración
./run_tests.sh integration

# Con reporte de cobertura
./run_tests.sh coverage

# Modo rápido
./run_tests.sh fast

# Ver ayuda
./run_tests.sh help
```

---

## 📊 Estructura Visual de Tests

```
backend/
│
├── 📝 conftest.py          ← Fixtures globales
│   ├── test_db            → BD en memoria
│   ├── client             → TestClient FastAPI
│   ├── sample_task_data   → Datos de ejemplo
│   └── create_sample_task → Tarea precreada
│
├── 🔧 test_crud.py         ← Tests Unitarios (21 tests)
│   ├── TestCreateTask     → 3 tests
│   ├── TestReadTask       → 4 tests
│   ├── TestFilterTasks    → 4 tests
│   ├── TestUpdateTask     → 4 tests
│   ├── TestDeleteTask     → 3 tests
│   └── TestDeleteAndCount → 3 tests
│
├── 🌐 test_api.py          ← Tests Integración (25 tests)
│   ├── TestRootEndpoint        → 2 tests
│   ├── TestCreateTaskEndpoint  → 5 tests
│   ├── TestListTasksEndpoint   → 5 tests
│   ├── TestGetTaskByIdEndpoint → 2 tests
│   ├── TestUpdateTaskEndpoint  → 6 tests
│   ├── TestDeleteTaskEndpoint  → 3 tests
│   └── TestCompleteWorkflow    → 2 tests
│
└── ✅ test_schemas.py      ← Tests Validación (11 tests)
    ├── TestTaskCreateSchema → 6 tests
    ├── TestTaskUpdateSchema → 4 tests
    └── TestTaskResponseSchema → 3 tests
```

---

## 💡 Tips y Trucos

### 🔍 Debug de un test que falla
```bash
# Ver traceback completo
pytest test_api.py::test_create_task_success -vv

# Ver prints y variables
pytest test_api.py::test_create_task_success -s

# Entrar en debugger al fallar
pytest --pdb
```

### 📈 Análisis de cobertura
```bash
# Generar reporte HTML
pytest --cov=. --cov-report=html

# Solo mostrar líneas no cubiertas
pytest --cov=. --cov-report=term-missing

# Ignorar archivos de test en cobertura
pytest --cov=. --cov-report=term --cov-config=.coveragerc
```

### ⚡ Optimizar velocidad
```bash
# Ejecutar tests en paralelo (requiere pytest-xdist)
pip install pytest-xdist
pytest -n auto

# Ejecutar solo tests que fallaron la última vez
pytest --lf

# Ejecutar primero los que fallaron
pytest --ff
```

---

## 🧪 Anatomía de un Test

```python
def test_create_task_success(client):
    """Descripción clara del test"""
    
    # 1. ARRANGE - Preparar datos
    task_data = {
        "title": "Nueva tarea",
        "completed": False
    }
    
    # 2. ACT - Ejecutar acción
    response = client.post("/tasks", json=task_data)
    
    # 3. ASSERT - Verificar resultado
    assert response.status_code == 201
    assert response.json()["title"] == "Nueva tarea"
```

---

## 🎓 Conceptos Clave

### ✨ Fixtures
```python
@pytest.fixture
def client(test_db):
    """Cliente de test con BD en memoria"""
    # Setup
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)
    
    yield client  # ← Test usa este cliente
    
    # Teardown automático
```

### 🔒 Aislamiento de Tests
- Cada test usa una **BD nueva en memoria**
- No comparten estado entre tests
- Orden de ejecución no importa

### ⚡ Base de Datos en Memoria
```python
# Mucho más rápido que SQLite en disco
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
```

---

## 📚 Documentación Relacionada

| Documento | Contenido |
|-----------|-----------|
| [TESTING.md](TESTING.md) | Guía completa de testing |
| [TEST_SUMMARY.md](TEST_SUMMARY.md) | Resumen detallado de todos los tests |
| [README.md](README.md) | Documentación general de la API |

---

## ✅ Checklist de Testing

Antes de hacer commit:

- [ ] Todos los tests pasan: `pytest`
- [ ] Cobertura > 90%: `pytest --cov=.`
- [ ] Sin warnings: `pytest --strict-warnings`
- [ ] Code style: `black .` (opcional)
- [ ] Linting: `flake8 .` (opcional)

---

## 🆘 Troubleshooting

### ❌ Error: "No module named 'pytest'"
```bash
pip install -r test_requirements.txt
```

### ❌ Error: "database is locked"
Verifica que uses `sqlite:///:memory:` en tests (ya configurado en `conftest.py`).

### ❌ Tests pasan individualmente pero fallan juntos
Los tests no son independientes. Verifica que no compartan estado.

### ❌ Import errors
```bash
# Asegúrate de estar en el directorio correcto
cd backend
pytest
```

---

**¡Feliz Testing!** 🚀✨

---

> 💡 **Tip**: Para validar cambios rápidamente, usa:
> ```bash
> pytest -x -v  # Detener en primer error con output verbose
> ```
