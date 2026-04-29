from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0)
    grade: float = Field(..., ge=0, le=5)


# StudentResponse: modelo Pydantic para la respuesta de la API
# Hereda de Student para incluir los mismos campos (name, age, grade)
# y añade el campo 'id' que se genera al guardar en la base de datos
class StudentResponse(Student):
    id: int

    # class Config: configuración interna de Pydantic
    # from_attributes = True: permite crear el modelo desde un objeto ORM
    # Esto es necesario porque los datos vienen de SQLAlchemy (objetos con atributos)
    # y Pydantic necesita saber cómo convertirlos a JSON
    class Config:
        from_attributes = True