"""
Tests unitarios para los esquemas Pydantic (validación de datos).
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from schemas import TaskCreate, TaskUpdate, TaskResponse


class TestTaskCreateSchema:
    """Tests para el schema de creación de tareas"""
    
    def test_valid_task_creation(self):
        """Crear schema válido con todos los campos"""
        task = TaskCreate(
            title="Tarea válida",
            description="Descripción",
            due_date=datetime(2025, 10, 30, 10, 0, 0),
            completed=False
        )
        
        assert task.title == "Tarea válida"
        assert task.description == "Descripción"
        assert task.completed is False
    
    def test_minimal_task_creation(self):
        """Crear schema solo con campos requeridos"""
        task = TaskCreate(title="Solo título")
        
        assert task.title == "Solo título"
        assert task.description is None
        assert task.due_date is None
        assert task.completed is False
    
    def test_missing_title_raises_error(self):
        """Validar que título es obligatorio"""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)
    
    def test_empty_title_raises_error(self):
        """Validar que título no puede estar vacío"""
        with pytest.raises(ValidationError):
            TaskCreate(title="")
    
    def test_title_too_long(self):
        """Validar límite de longitud del título"""
        long_title = "a" * 300  # Más de 255 caracteres
        
        with pytest.raises(ValidationError):
            TaskCreate(title=long_title)
    
    def test_invalid_date_type(self):
        """Validar que fecha debe ser datetime"""
        with pytest.raises(ValidationError):
            TaskCreate(
                title="Tarea",
                due_date="fecha-invalida"
            )


class TestTaskUpdateSchema:
    """Tests para el schema de actualización de tareas"""
    
    def test_update_all_fields(self):
        """Actualizar todos los campos"""
        update = TaskUpdate(
            title="Nuevo título",
            description="Nueva descripción",
            due_date=datetime(2025, 11, 1, 15, 0, 0),
            completed=True
        )
        
        assert update.title == "Nuevo título"
        assert update.description == "Nueva descripción"
        assert update.completed is True
    
    def test_update_single_field(self):
        """Actualizar solo un campo (los demás None)"""
        update = TaskUpdate(completed=True)
        
        assert update.completed is True
        assert update.title is None
        assert update.description is None
    
    def test_update_empty_is_valid(self):
        """Schema de actualización vacío es válido"""
        update = TaskUpdate()
        
        assert update.title is None
        assert update.description is None
        assert update.completed is None
    
    def test_update_with_empty_title_fails(self):
        """Título vacío no es válido en actualización"""
        with pytest.raises(ValidationError):
            TaskUpdate(title="")


class TestTaskResponseSchema:
    """Tests para el schema de respuesta"""
    
    def test_response_from_dict(self):
        """Crear respuesta desde diccionario"""
        data = {
            "id": 1,
            "title": "Tarea",
            "description": "Descripción",
            "due_date": datetime(2025, 10, 30, 10, 0, 0),
            "completed": False,
            "created_at": datetime.now()
        }
        
        response = TaskResponse(**data)
        
        assert response.id == 1
        assert response.title == "Tarea"
        assert response.completed is False
    
    def test_response_requires_id(self):
        """ID es obligatorio en respuesta"""
        with pytest.raises(ValidationError) as exc_info:
            TaskResponse(
                title="Sin ID",
                completed=False,
                created_at=datetime.now()
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("id",) for error in errors)
    
    def test_response_requires_created_at(self):
        """created_at es obligatorio en respuesta"""
        with pytest.raises(ValidationError):
            TaskResponse(
                id=1,
                title="Sin created_at",
                completed=False
            )
