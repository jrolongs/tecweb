# Importación de FastAPI y CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Importación del router de estudiantes
# students.py contiene todas las rutas relacionadas con estudiantes
from app.routes import students, email, auth
from app.services.auth_service import get_current_user
from fastapi import Depends

# Importación de engine y Base para crear las tablas
# engine: conexión a la base de datos SQLite
# Base: clase base para los modelos ORM
from app.database import engine, Base

# Importación de los middlewares
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.audit_middleware import AuditMiddleware

# create_all(): crea todas las tablas definidas en los modelos
# Se ejecuta al iniciar la app y crea el archivo 'students.db' si no existe
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Middleware CORS para permitir solicitudes del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de middlewares
# El orden de add_middleware determina el orden de ejecución:
# 1. RateLimitMiddleware - primero (más cercano al cliente)
# 2. AuditMiddleware - segundo
# 3. LoggingMiddleware - último (más cercano a la app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)

# Registro del router de estudiantes
# Todas las rutas de students.py estarán disponibles en /students
# Las rutas de students requieren autenticación con token Bearer
app.include_router(students.router, dependencies=[Depends(get_current_user)])
app.include_router(email.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/app", include_in_schema=False)
def frontend_app():
    return FileResponse(FRONTEND_DIR / "index.html")
