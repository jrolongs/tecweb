# Importaciones de SQLAlchemy
# create_engine: crea el motor de conexión a la base de datos
# sessionmaker: crea sesiones para interactuar con la base de datos
# declarative_base: clase base para definir modelos ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a SQLite
# sqlite:///./students.db crea un archivo 'students.db' en la raíz del proyecto
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"

# engine: objeto que gestiona la conexión a la base de datos
# connect_args={"check_same_thread": False} permite acceso desde múltiples hilos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: fábrica de sesiones de base de datos
# autocommit=False: los cambios no se confirman automáticamente
# autoflush=False: los cambios no se envían automáticamente a la DB
# bind=engine: asocia el motor de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base para todos los modelos ORM
# Se usa para crear las tablas automáticamente
Base = declarative_base()


# Función generadora para obtener la sesión de DB en cada request
# Se usa como dependencia en FastAPI con Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna la sesión al endpoint
    finally:
        db.close()  # Cierra la sesión al terminar