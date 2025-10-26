"""
Configuración de la base de datos SQLite con SQLAlchemy.
Este módulo gestiona la conexión y sesiones a la base de datos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a SQLite (archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./quicktask.db"

# Crear el motor de base de datos
# check_same_thread=False es necesario para SQLite con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos
Base = declarative_base()


def get_db():
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    Garantiza que la sesión se cierre después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
