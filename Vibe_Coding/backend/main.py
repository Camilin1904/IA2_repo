"""
API REST de QuickTask - Gestión de Tareas
FastAPI application con endpoints CRUD completos.
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

import models
import schemas
import crud
from database import engine, get_db

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="QuickTask API",
    description="API REST para gestión de tareas personales",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz - Información de la API.
    """
    return {
        "message": "Bienvenido a QuickTask API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/tasks", response_model=schemas.TaskListResponse, tags=["Tasks"])
def list_tasks(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de tareas"),
    completed: Optional[bool] = Query(None, description="Filtrar por estado completado"),
    search: Optional[str] = Query(None, description="Buscar en título o descripción"),
    db: Session = Depends(get_db)
):
    """
    **Listar todas las tareas** con opciones de filtrado y paginación.
    
    - **skip**: Omitir N tareas (para paginación)
    - **limit**: Máximo de tareas a retornar
    - **completed**: Filtrar por estado (true/false/null)
    - **search**: Buscar texto en título o descripción
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, completed=completed, search=search)
    total = crud.count_tasks(db, completed=completed, search=search)
    
    return schemas.TaskListResponse(total=total, tasks=tasks)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    **Obtener una tarea específica** por su ID.
    
    - **task_id**: ID de la tarea a consultar
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    **Crear una nueva tarea**.
    
    Campos obligatorios:
    - **title**: Título de la tarea (1-255 caracteres)
    
    Campos opcionales:
    - **description**: Descripción detallada
    - **due_date**: Fecha de vencimiento (formato ISO 8601)
    - **completed**: Estado inicial (por defecto false)
    """
    return crud.create_task(db=db, task=task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_full(
    task_id: int, 
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db)
):
    """
    **Actualizar completamente una tarea** (todos los campos requeridos).
    
    - **task_id**: ID de la tarea a actualizar
    - Requiere todos los campos del objeto tarea
    """
    task_update = schemas.TaskUpdate(**task.model_dump())
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_partial(
    task_id: int, 
    task: schemas.TaskUpdate, 
    db: Session = Depends(get_db)
):
    """
    **Actualizar parcialmente una tarea** (solo campos proporcionados).
    
    - **task_id**: ID de la tarea a actualizar
    - Solo envía los campos que deseas modificar
    
    Útil para operaciones como:
    - Marcar como completada: `{"completed": true}`
    - Cambiar título: `{"title": "Nuevo título"}`
    """
    db_task = crud.update_task(db, task_id=task_id, task_update=task)
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    **Eliminar una tarea** permanentemente.
    
    - **task_id**: ID de la tarea a eliminar
    - Retorna 204 No Content si se eliminó exitosamente
    """
    success = crud.delete_task(db, task_id=task_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    return None


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de salud para verificar que la API está funcionando.
    """
    return {"status": "healthy", "service": "QuickTask API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
