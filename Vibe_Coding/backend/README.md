# 🚀 QuickTask API - Backend

API REST construida con **FastAPI** para gestionar tareas personales del proyecto **QuickTask**.

## 📁 Estructura del Proyecto

```
backend/
├── main.py           # Aplicación principal con endpoints
├── models.py         # Modelos SQLAlchemy (DB)
├── schemas.py        # Esquemas Pydantic (validación)
├── crud.py           # Operaciones CRUD
├── database.py       # Configuración de SQLite
├── requirements.txt  # Dependencias
└── README.md         # Este archivo
```

## 🔧 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar el Servidor

### Opción 1: Local (Python)

```bash
# Usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O ejecutar main.py
python main.py
```

### Opción 2: Docker (Recomendado)

```bash
# Levantar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Opción 3: Script Helper

```bash
# Desarrollo con hot-reload
./docker.sh up

# Ver estado
./docker.sh status
```

**📖 Ver guía completa:** [DOCKER.md](DOCKER.md)

---

El servidor estará disponible en: **http://localhost:8000**

- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## 📡 Endpoints Disponibles

### 🔍 Listar Tareas
```bash
# Listar todas las tareas
curl -X GET "http://localhost:8000/tasks"

# Listar solo tareas pendientes
curl -X GET "http://localhost:8000/tasks?completed=false"

# Listar tareas completadas
curl -X GET "http://localhost:8000/tasks?completed=true"

# Buscar tareas con texto
curl -X GET "http://localhost:8000/tasks?search=compras"

# Paginación (omitir 10, máximo 20)
curl -X GET "http://localhost:8000/tasks?skip=10&limit=20"
```

### ➕ Crear Tarea
```bash
# Crear tarea simple
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar víveres",
    "description": "Leche, pan y huevos",
    "due_date": "2025-10-30T10:00:00",
    "completed": false
  }'

# Crear tarea mínima (solo título)
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Llamar al médico"}'
```

### 📄 Obtener Tarea por ID
```bash
curl -X GET "http://localhost:8000/tasks/1"
```

### ✏️ Actualizar Tarea Completa (PUT)
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar víveres (URGENTE)",
    "description": "Leche, pan, huevos y café",
    "due_date": "2025-10-28T10:00:00",
    "completed": false
  }'
```

### ✏️ Actualizar Tarea Parcial (PATCH)
```bash
# Marcar como completada
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Cambiar solo el título
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nuevo título"}'

# Actualizar fecha de vencimiento
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"due_date": "2025-11-01T15:30:00"}'
```

### 🗑️ Eliminar Tarea
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## 🧪 Probar la API

### Usando cURL (ejemplos completos)

```bash
# 1. Crear tres tareas
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudiar FastAPI", "description": "Completar tutorial oficial"}'

curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacer ejercicio", "due_date": "2025-10-27T07:00:00"}'

curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Leer documentación SQLAlchemy", "completed": false}'

# 2. Listar todas las tareas
curl -X GET "http://localhost:8000/tasks"

# 3. Marcar la tarea #1 como completada
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# 4. Ver solo tareas pendientes
curl -X GET "http://localhost:8000/tasks?completed=false"

# 5. Eliminar la tarea #2
curl -X DELETE "http://localhost:8000/tasks/2"
```

### Usando Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Crear tarea
response = requests.post(f"{BASE_URL}/tasks", json={
    "title": "Mi nueva tarea",
    "description": "Descripción de prueba"
})
print(response.json())

# Listar tareas
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())

# Actualizar tarea
response = requests.patch(f"{BASE_URL}/tasks/1", json={"completed": True})
print(response.json())
```

## 🗄️ Base de Datos

- **Motor**: SQLite
- **Archivo**: `quicktask.db` (se crea automáticamente)
- **ORM**: SQLAlchemy

### Esquema de la Tabla `tasks`

| Campo       | Tipo      | Descripción                          |
|-------------|-----------|--------------------------------------|
| id          | INTEGER   | Primary Key (autoincremental)        |
| title       | VARCHAR   | Título de la tarea (obligatorio)     |
| description | TEXT      | Descripción detallada (opcional)     |
| due_date    | DATETIME  | Fecha de vencimiento (opcional)      |
| completed   | BOOLEAN   | Estado de completado (default: false)|
| created_at  | DATETIME  | Fecha de creación (automática)       |

## ✅ Validaciones (Pydantic)

- **title**: Requerido, entre 1-255 caracteres
- **description**: Opcional, texto libre
- **due_date**: Opcional, formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- **completed**: Boolean, por defecto `false`

## 📝 Notas Técnicas

1. **Actualización Parcial vs Completa**:
   - `PUT /tasks/{id}`: Requiere todos los campos
   - `PATCH /tasks/{id}`: Solo campos que quieras modificar

2. **Filtros de búsqueda**:
   - Búsqueda case-insensitive en título y descripción
   - Filtro por estado (`completed=true/false`)

3. **Paginación**:
   - `skip`: Omitir N registros
   - `limit`: Máximo 500 tareas por request

4. **Formatos de fecha**:
   ```
   2025-10-30T10:00:00       # Fecha y hora
   2025-10-30T10:00:00Z      # UTC
   2025-10-30T10:00:00-05:00 # Con zona horaria
   ```

## 🧪 Testing

El proyecto incluye **57 tests automatizados** con pytest.

### Ejecutar todos los tests

```bash
# Instalar dependencias de testing
pip install -r test_requirements.txt

# Ejecutar tests
pytest

# Con cobertura de código
pytest --cov=. --cov-report=html
```

### Tipos de tests incluidos

- ✅ **Tests unitarios** (`test_crud.py`): 21 tests de lógica CRUD
- ✅ **Tests de integración** (`test_api.py`): 25 tests de endpoints HTTP
- ✅ **Tests de validación** (`test_schemas.py`): 11 tests de Pydantic

**📖 Ver guía completa:** [TESTING.md](TESTING.md)

### Cobertura actual

- **CRUD Operations**: ~95%
- **API Endpoints**: ~90%
- **Schemas**: ~85%
- **Total**: ~90%

## � Despliegue con Docker

El proyecto incluye configuración completa de Docker:

```bash
# Levantar contenedor
docker-compose up -d

# Ver documentación completa
cat DOCKER.md
```

**Archivos incluidos:**
- ✅ `Dockerfile` - Imagen básica
- ✅ `Dockerfile.prod` - Imagen optimizada
- ✅ `docker-compose.yml` - Compose estándar
- ✅ `docker-compose.dev.yml` - Con hot-reload
- ✅ `docker-compose.prod.yml` - Producción
- ✅ `docker.sh` - Script de gestión

**📖 Ver guía completa:** [DOCKER.md](DOCKER.md)

## �🚧 Mejoras Futuras

- [ ] Autenticación JWT
- [ ] Filtro por rango de fechas
- [ ] Categorías/etiquetas
- [ ] Soft delete (eliminación lógica)
- [ ] Paginación con cursores
- [ ] Rate limiting
- [x] Tests unitarios e integración
- [x] Docker y Docker Compose

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Pytest Docs](https://docs.pytest.org/)

---

**Desarrollado para el proyecto QuickTask** 🎯
