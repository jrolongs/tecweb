# Importaciones de FastAPI y SQLAlchemy
# HTTPException: para devolver errores HTTP (404, etc.)
# Depends: para injectar dependencias (sesión de DB)
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# Student: modelo Pydantic para validación de datos de entrada
from app.models.student_model import Student

# StudentDB: modelo ORM de SQLAlchemy (tabla en la DB)
# Se renombra para distinguir del modelo Pydantic
from app.models.db_models import Student as StudentDB

# get_db: función para obtener la sesión de base de datos
from app.database import get_db


# StudentController: clase que contiene la lógica de negocio
# Todas sus funciones son staticmethod (no necesitan instancia)
class StudentController:
    
    # get_all(): obtiene todos los estudiantes de la base de datos
    # db: sesión de SQLAlchemy injectada automáticamente por Depends(get_db)
    @staticmethod
    def get_all(db: Session = Depends(get_db)) -> list[StudentDB]:
        # query(StudentDB).all() ejecuta SELECT * FROM students
        return db.query(StudentDB).all()

    
    # get_by_id(): obtiene un estudiante por su ID
    # student_id: identificador del estudiante a buscar
    @staticmethod
    def get_by_id(student_id: int, db: Session = Depends(get_db)) -> StudentDB:
        # filter() añade condición WHERE id = student_id
        # first() devuelve el primer resultado o None
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        
        # Si no existe el estudiante, devuelve error 404
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return student

    
    # create(): crea un nuevo estudiante en la base de datos
    # student: objeto Pydantic con los datos validados
    @staticmethod
    def create(student: Student, db: Session = Depends(get_db)) -> StudentDB:
        # Convierte el modelo Pydantic a diccionario y crea instancia de StudentDB
        new_student = StudentDB(**student.model_dump())
        
        # db.add() prepara el objeto para ser insertado
        db.add(new_student)
        
        # db.commit() confirma los cambios en la base de datos
        db.commit()
        
        # db.refresh() actualiza el objeto con el ID generado por SQLite
        db.refresh(new_student)
        return new_student

    
    # update(): actualiza los datos de un estudiante existente
    # student_id: ID del estudiante a actualizar
    # updated_data: nuevos datos para el estudiante
    @staticmethod
    def update(student_id: int, updated_data: Student, db: Session = Depends(get_db)) -> StudentDB:
        # Busca el estudiante por ID
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        
        # Si no existe, devuelve error 404
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Actualiza los campos del estudiante
        student.name = updated_data.name
        student.age = updated_data.age
        student.grade = updated_data.grade
        
        # Confirma los cambios en la DB
        db.commit()
        
        # Actualiza el objeto con los datos guardados
        db.refresh(student)
        return student

    
    # delete(): elimina un estudiante de la base de datos
    # student_id: ID del estudiante a eliminar
    @staticmethod
    def delete(student_id: int, db: Session = Depends(get_db)) -> dict:
        # Busca el estudiante por ID
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        
        # Si no existe, devuelve error 404
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # db.delete() marca el objeto para eliminación
        db.delete(student)
        
        # Confirma la eliminación en la base de datos
        db.commit()
        return {"message": "Estudiante eliminado"}