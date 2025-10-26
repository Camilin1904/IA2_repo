"""
Modelos de base de datos para QuickTask.
Define la estructura de la tabla 'tasks' en SQLite.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base


class Task(Base):
    """
    Modelo de Tarea para la base de datos.
    
    Atributos:
        id: Identificador único de la tarea (clave primaria)
        title: Título de la tarea (obligatorio)
        description: Descripción detallada de la tarea (opcional)
        due_date: Fecha de vencimiento (opcional)
        completed: Estado de completado (por defecto False)
        created_at: Fecha de creación (automática)
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
