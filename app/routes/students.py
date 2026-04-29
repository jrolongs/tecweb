# Importaciones de FastAPI y SQLAlchemy
# APIRouter: permite definir rutas modulares
# Depends: para injectar la sesión de base de datos
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Student: modelo Pydantic para datos de entrada (sin ID)
# StudentResponse: modelo Pydantic para respuesta (con ID)
from app.models.student_model import Student, StudentResponse

# StudentController: lógica de negocio para estudiantes
from app.controllers.student_controller import StudentController

# get_db: función para obtener la sesión de base de datos
from app.database import get_db

# router: objeto que define las rutas de estudiantes
# prefix="/students": todas las rutas empezar por /students
# tags=["Estudiantes"]: grupo en la documentación automática
router = APIRouter(prefix="/students", tags=["Estudiantes"])


# GET /students/ - Obtiene todos los estudiantes
# response_model: define el formato de respuesta JSON
@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    # Llama al controller para obtener todos los registros de la DB
    return StudentController.get_all(db)


# GET /students/{student_id} - Obtiene un estudiante por su ID
# student_id: parámetro de路径 (path parameter)
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    # Llama al controller para buscar por ID
    return StudentController.get_by_id(student_id, db)


# POST /students/ - Crea un nuevo estudiante
# student: cuerpo de la solicitud (JSON) validado por Pydantic
@router.post("/", response_model=StudentResponse)
def create_student(student: Student, db: Session = Depends(get_db)):
    # Llama al controller para crear el registro
    return StudentController.create(student, db)


# PUT /students/{student_id} - Actualiza un estudiante existente
# student_id: ID del estudiante a actualizar
# updated_data: nuevos datos (JSON) validados por Pydantic
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, updated_data: Student, db: Session = Depends(get_db)):
    # Llama al controller para actualizar el registro
    return StudentController.update(student_id, updated_data, db)


# DELETE /students/{student_id} - Elimina un estudiante
# student_id: ID del estudiante a eliminar
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    # Llama al controller para eliminar el registro
    return StudentController.delete(student_id, db)