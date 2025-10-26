"""
Operaciones CRUD (Create, Read, Update, Delete) para tareas.
Contiene la lógica de negocio para interactuar con la base de datos.
"""
from sqlalchemy.orm import Session
from typing import Optional
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    Obtiene una tarea por su ID.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a buscar
    
    Returns:
        Task o None si no existe
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    completed: Optional[bool] = None,
    search: Optional[str] = None
) -> list[Task]:
    """
    Obtiene una lista de tareas con filtros opcionales.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a omitir (paginación)
        limit: Número máximo de registros a retornar
        completed: Filtrar por estado (True/False/None para todos)
        search: Buscar en título o descripción
    
    Returns:
        Lista de tareas
    """
    query = db.query(Task)
    
    # Filtro por estado de completado
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    # Filtro de búsqueda por texto
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_pattern)) | 
            (Task.description.ilike(search_pattern))
        )
    
    return query.offset(skip).limit(limit).all()


def count_tasks(
    db: Session,
    completed: Optional[bool] = None,
    search: Optional[str] = None
) -> int:
    """
    Cuenta el número total de tareas con filtros opcionales.
    
    Args:
        db: Sesión de base de datos
        completed: Filtrar por estado
        search: Buscar en título o descripción
    
    Returns:
        Número total de tareas
    """
    query = db.query(Task)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_pattern)) | 
            (Task.description.ilike(search_pattern))
        )
    
    return query.count()


def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Crea una nueva tarea en la base de datos.
    
    Args:
        db: Sesión de base de datos
        task: Datos de la tarea a crear
    
    Returns:
        La tarea creada con su ID generado
    """
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Actualiza una tarea existente.
    Solo actualiza los campos proporcionados (actualización parcial).
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a actualizar
        task_update: Datos a actualizar
    
    Returns:
        La tarea actualizada o None si no existe
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Elimina una tarea de la base de datos.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a eliminar
    
    Returns:
        True si se eliminó, False si no existía
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True
