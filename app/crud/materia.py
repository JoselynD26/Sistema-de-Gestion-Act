from sqlalchemy.orm import Session
from app.models.materia import Materia
from app.models.carrera import Carrera
from app.models.sede import Sede
from app.models.docente import Docente
from app.schemas.materia import MateriaCreate

def crear_materia(db: Session, datos: MateriaCreate):
    nueva = Materia(nombre=datos.nombre)

    if datos.carrera_ids:
        carreras = db.query(Carrera).filter(Carrera.id.in_(datos.carrera_ids)).all()
        nueva.carreras = carreras

    if datos.sede_ids:
        sedes = db.query(Sede).filter(Sede.id.in_(datos.sede_ids)).all()
        nueva.sedes = sedes

    if datos.docente_ids:
        docentes = db.query(Docente).filter(Docente.id.in_(datos.docente_ids)).all()
        nueva.docentes = docentes

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_materias_por_sede(db: Session, id_sede: int):
    return (
        db.query(Materia)
        .join(Materia.sedes)
        .filter(Sede.id == id_sede)
        .all()
    )
    
def listar_materias(db: Session):
    return db.query(Materia).all()

def obtener_materia(db: Session, materia_id: int):
    return db.query(Materia).filter(Materia.id == materia_id).first()

def actualizar_materia(db: Session, id_materia: int, materia_data: MateriaCreate):
    materia = db.query(Materia).filter(Materia.id == id_materia).first()
    if not materia:
        return None

    # Actualizar nombre
    materia.nombre = materia_data.nombre

    # Actualizar relaciones (si vienen vacías, se limpian)
    materia.carreras = db.query(Carrera).filter(Carrera.id.in_(materia_data.carrera_ids)).all() if materia_data.carrera_ids else []
    materia.sedes = db.query(Sede).filter(Sede.id.in_(materia_data.sede_ids)).all() if materia_data.sede_ids else []
    materia.docentes = db.query(Docente).filter(Docente.id.in_(materia_data.docente_ids)).all() if materia_data.docente_ids else []

    db.commit()
    db.refresh(materia)
    return materia

def eliminar_materia(db: Session, materia_id: int):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if materia:
        db.delete(materia)
        db.commit()
    return materia