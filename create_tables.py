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
    # docente_carrera,  # Eliminado por conflicto/redundancia
    # docente_materia,  # Eliminado por conflicto/redundancia
    docente_sala,
    docente_vinculacion,
    escritorio,
    horario,
    materia,
    # materia_carrera, # Eliminado por conflicto/redundancia
    notificacion,
    permiso,
    plaza,
    reserva,
    relaciones,
    rol,
    rol_permiso,
    sala,
    # sala_carrera,    # Eliminado por conflicto/redundancia
    # sala_profesores, # (Mantener si es único, pero verificar) -> sala_profesores es una TABLA normal o modelo? Es un modelo, ok.
    sala_profesores,
    sede,
    # sede_sala,       # Eliminado por redundancia (está en relaciones)
    usuario,
    usuario_rol, 
)

# Crear todas las tablas en la base de datos
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")