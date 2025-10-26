"""
Esquemas Pydantic para validación de datos.
Define la estructura de entrada/salida de la API.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    """
    Schema base con los campos comunes de una tarea.
    """
    title: str = Field(..., min_length=1, max_length=255, description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción opcional de la tarea")
    due_date: Optional[datetime] = Field(None, description="Fecha de vencimiento (formato ISO 8601)")
    completed: bool = Field(default=False, description="Estado de completado")


class TaskCreate(TaskBase):
    """
    Schema para crear una nueva tarea.
    Hereda todos los campos de TaskBase.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema para actualizar una tarea existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Schema de respuesta que incluye los campos generados por la BD.
    """
    id: int
    created_at: datetime
    
    # Configuración para Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """
    Schema para la respuesta de listado de tareas.
    """
    total: int
    tasks: list[TaskResponse]
