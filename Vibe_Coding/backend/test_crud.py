"""
Tests unitarios para las operaciones CRUD (crud.py).
Prueban la lógica de negocio de forma aislada.
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session

import crud
from schemas import TaskCreate, TaskUpdate
from models import Task


class TestCreateTask:
    """Tests para la creación de tareas"""
    
    def test_create_task_with_all_fields(self, test_db: Session):
        """Crear tarea con todos los campos completos"""
        task_data = TaskCreate(
            title="Comprar víveres",
            description="Leche, pan y huevos",
            due_date=datetime(2025, 10, 30, 10, 0, 0),
            completed=False
        )
        
        task = crud.create_task(test_db, task_data)
        
        assert task.id is not None
        assert task.title == "Comprar víveres"
        assert task.description == "Leche, pan y huevos"
        assert task.completed is False
        assert task.created_at is not None
    
    def test_create_task_minimal(self, test_db: Session):
        """Crear tarea solo con título (campos mínimos)"""
        task_data = TaskCreate(title="Llamar al médico")
        
        task = crud.create_task(test_db, task_data)
        
        assert task.id is not None
        assert task.title == "Llamar al médico"
        assert task.description is None
        assert task.due_date is None
        assert task.completed is False
    
    def test_create_multiple_tasks(self, test_db: Session):
        """Crear múltiples tareas y verificar IDs únicos"""
        task1 = crud.create_task(test_db, TaskCreate(title="Tarea 1"))
        task2 = crud.create_task(test_db, TaskCreate(title="Tarea 2"))
        
        assert task1.id != task2.id
        assert task1.title == "Tarea 1"
        assert task2.title == "Tarea 2"


class TestReadTask:
    """Tests para la lectura de tareas"""
    
    def test_get_task_by_id(self, test_db: Session):
        """Obtener tarea existente por ID"""
        # Crear tarea
        task_data = TaskCreate(title="Tarea de prueba")
        created_task = crud.create_task(test_db, task_data)
        
        # Recuperar tarea
        retrieved_task = crud.get_task(test_db, created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == "Tarea de prueba"
    
    def test_get_nonexistent_task(self, test_db: Session):
        """Intentar obtener tarea que no existe"""
        task = crud.get_task(test_db, 9999)
        assert task is None
    
    def test_get_all_tasks(self, test_db: Session):
        """Obtener lista de todas las tareas"""
        # Crear 3 tareas
        crud.create_task(test_db, TaskCreate(title="Tarea 1"))
        crud.create_task(test_db, TaskCreate(title="Tarea 2"))
        crud.create_task(test_db, TaskCreate(title="Tarea 3"))
        
        tasks = crud.get_tasks(test_db)
        
        assert len(tasks) == 3
        assert all(isinstance(task, Task) for task in tasks)
    
    def test_get_tasks_with_pagination(self, test_db: Session):
        """Probar paginación en listado de tareas"""
        # Crear 5 tareas
        for i in range(5):
            crud.create_task(test_db, TaskCreate(title=f"Tarea {i+1}"))
        
        # Obtener primeras 2
        tasks_page1 = crud.get_tasks(test_db, skip=0, limit=2)
        assert len(tasks_page1) == 2
        
        # Obtener siguientes 2
        tasks_page2 = crud.get_tasks(test_db, skip=2, limit=2)
        assert len(tasks_page2) == 2
        
        # Verificar que son diferentes
        assert tasks_page1[0].id != tasks_page2[0].id


class TestFilterTasks:
    """Tests para filtrado de tareas"""
    
    def test_filter_by_completed_status(self, test_db: Session):
        """Filtrar tareas por estado completado"""
        # Crear tareas con diferentes estados
        crud.create_task(test_db, TaskCreate(title="Pendiente 1", completed=False))
        crud.create_task(test_db, TaskCreate(title="Completada 1", completed=True))
        crud.create_task(test_db, TaskCreate(title="Pendiente 2", completed=False))
        
        # Filtrar pendientes
        pending_tasks = crud.get_tasks(test_db, completed=False)
        assert len(pending_tasks) == 2
        assert all(not task.completed for task in pending_tasks)
        
        # Filtrar completadas
        completed_tasks = crud.get_tasks(test_db, completed=True)
        assert len(completed_tasks) == 1
        assert all(task.completed for task in completed_tasks)
    
    def test_search_by_title(self, test_db: Session):
        """Buscar tareas por texto en título"""
        crud.create_task(test_db, TaskCreate(title="Comprar víveres"))
        crud.create_task(test_db, TaskCreate(title="Hacer ejercicio"))
        crud.create_task(test_db, TaskCreate(title="Comprar medicamentos"))
        
        # Buscar tareas con "comprar"
        results = crud.get_tasks(test_db, search="comprar")
        assert len(results) == 2
        assert all("comprar" in task.title.lower() for task in results)
    
    def test_search_by_description(self, test_db: Session):
        """Buscar tareas por texto en descripción"""
        crud.create_task(test_db, TaskCreate(
            title="Tarea 1",
            description="Ir al supermercado"
        ))
        crud.create_task(test_db, TaskCreate(
            title="Tarea 2",
            description="Ir al gimnasio"
        ))
        
        results = crud.get_tasks(test_db, search="gimnasio")
        assert len(results) == 1
        assert "gimnasio" in results[0].description.lower()
    
    def test_count_tasks(self, test_db: Session):
        """Contar tareas con filtros"""
        crud.create_task(test_db, TaskCreate(title="Tarea 1", completed=False))
        crud.create_task(test_db, TaskCreate(title="Tarea 2", completed=True))
        crud.create_task(test_db, TaskCreate(title="Tarea 3", completed=False))
        
        total = crud.count_tasks(test_db)
        assert total == 3
        
        pending_count = crud.count_tasks(test_db, completed=False)
        assert pending_count == 2


class TestUpdateTask:
    """Tests para actualización de tareas"""
    
    def test_update_task_title(self, test_db: Session):
        """Actualizar solo el título de una tarea"""
        # Crear tarea
        task = crud.create_task(test_db, TaskCreate(title="Título original"))
        
        # Actualizar título
        update_data = TaskUpdate(title="Título actualizado")
        updated_task = crud.update_task(test_db, task.id, update_data)
        
        assert updated_task is not None
        assert updated_task.title == "Título actualizado"
        assert updated_task.id == task.id
    
    def test_update_task_completed_status(self, test_db: Session):
        """Marcar tarea como completada"""
        task = crud.create_task(test_db, TaskCreate(title="Tarea pendiente"))
        
        # Marcar como completada
        update_data = TaskUpdate(completed=True)
        updated_task = crud.update_task(test_db, task.id, update_data)
        
        assert updated_task.completed is True
    
    def test_update_multiple_fields(self, test_db: Session):
        """Actualizar múltiples campos a la vez"""
        task = crud.create_task(test_db, TaskCreate(title="Original"))
        
        update_data = TaskUpdate(
            title="Actualizado",
            description="Nueva descripción",
            completed=True
        )
        updated_task = crud.update_task(test_db, task.id, update_data)
        
        assert updated_task.title == "Actualizado"
        assert updated_task.description == "Nueva descripción"
        assert updated_task.completed is True
    
    def test_update_nonexistent_task(self, test_db: Session):
        """Intentar actualizar tarea que no existe"""
        update_data = TaskUpdate(title="No existe")
        result = crud.update_task(test_db, 9999, update_data)
        
        assert result is None


class TestDeleteTask:
    """Tests para eliminación de tareas"""
    
    def test_delete_existing_task(self, test_db: Session):
        """Eliminar tarea existente"""
        # Crear tarea
        task = crud.create_task(test_db, TaskCreate(title="Para eliminar"))
        
        # Eliminar
        success = crud.delete_task(test_db, task.id)
        assert success is True
        
        # Verificar que no existe
        deleted_task = crud.get_task(test_db, task.id)
        assert deleted_task is None
    
    def test_delete_nonexistent_task(self, test_db: Session):
        """Intentar eliminar tarea que no existe"""
        success = crud.delete_task(test_db, 9999)
        assert success is False
    
    def test_delete_and_count(self, test_db: Session):
        """Verificar que el conteo se actualiza después de eliminar"""
        # Crear 3 tareas
        task1 = crud.create_task(test_db, TaskCreate(title="Tarea 1"))
        crud.create_task(test_db, TaskCreate(title="Tarea 2"))
        crud.create_task(test_db, TaskCreate(title="Tarea 3"))
        
        assert crud.count_tasks(test_db) == 3
        
        # Eliminar una
        crud.delete_task(test_db, task1.id)
        
        assert crud.count_tasks(test_db) == 2
