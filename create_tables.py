from app.core.config import Base, engine

# Importa todos los modelos para que SQLAlchemy los registre
from app.models import (
    aula,
    carrera,
    croquis,
    curso,
    curso_aula,
    curso_horario,
    docente,
    docente_carrera,
    docente_materia,
    docente_sala,
    docente_vinculacion,
    escritorio,
    horario,
    materia,
    materia_carrera,
    notificacion,
    permiso,
    plaza,
    reserva,
    relaciones,
    rol,
    rol_permiso,
    sala,
    sala_carrera,
    sala_profesores,
    sede,
    usuario,
    usuario_rol, 
)

# Crear todas las tablas en la base de datos
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")