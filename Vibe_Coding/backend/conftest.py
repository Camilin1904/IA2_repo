"""
Configuración global de pytest.
Define fixtures compartidos por todos los tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
import models


# URL de base de datos en memoria para tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """
    Fixture que crea una base de datos SQLite en memoria para cada test.
    Se destruye automáticamente al finalizar el test.
    
    Scope: function - Se crea una nueva BD para cada test (aislamiento total)
    """
    # Crear engine con configuración especial para SQLite en memoria
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Mantiene la conexión en memoria
    )
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión de prueba
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    # Limpiar: eliminar todas las tablas después del test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Fixture que proporciona un cliente de prueba de FastAPI
    con la base de datos de test inyectada.
    
    Args:
        test_db: Base de datos en memoria
    
    Returns:
        TestClient para hacer peticiones HTTP simuladas
    """
    def override_get_db():
        """Override de la dependencia get_db para usar la BD de test"""
        try:
            yield test_db
        finally:
            test_db.close()
    
    # Sobreescribir la dependencia de base de datos
    app.dependency_overrides[get_db] = override_get_db
    
    # Crear cliente de prueba
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar override
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_task_data():
    """
    Fixture que proporciona datos de ejemplo para crear tareas.
    """
    return {
        "title": "Tarea de prueba",
        "description": "Esta es una descripción de prueba",
        "due_date": "2025-10-30T10:00:00",
        "completed": False
    }


@pytest.fixture(scope="function")
def create_sample_task(client, sample_task_data):
    """
    Fixture que crea una tarea de ejemplo y retorna su respuesta.
    Útil para tests que necesitan una tarea existente.
    """
    response = client.post("/tasks", json=sample_task_data)
    return response.json()
