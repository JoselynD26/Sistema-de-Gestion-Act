from sqlalchemy.orm import Session, joinedload
from app.models.materia import Materia
from app.models.carrera import Carrera
from app.models.sede import Sede
from app.models.docente import Docente
from app.schemas.materia import MateriaCreate


def get_materias(db: Session):
    return db.query(Materia).all()


def get_materias_por_sede(db: Session, sede_id: int):
    return (
        db.query(Materia)
        .options(
            joinedload(Materia.carreras),
            joinedload(Materia.docentes),
            joinedload(Materia.sedes),
        )
        .filter(Materia.sedes.any(Sede.id == sede_id))
        .all()
    )


def get_materia(db: Session, materia_id: int):
    return db.query(Materia).filter(Materia.id == materia_id).first()


def create_materia(db: Session, materia: MateriaCreate):
    # Generar código automático si no viene
    codigo = materia.codigo or f"MAT{db.query(Materia).count() + 1:03d}"

    db_materia = Materia(
        nombre=materia.nombre,
        codigo=codigo,
    )

    # Relaciones
    if materia.carrera_ids:
        db_materia.carreras = (
            db.query(Carrera)
            .filter(Carrera.id.in_(materia.carrera_ids))
            .all()
        )

    if materia.sede_ids:
        db_materia.sedes = (
            db.query(Sede)
            .filter(Sede.id.in_(materia.sede_ids))
            .all()
        )

    if materia.docente_ids:
        db_materia.docentes = (
            db.query(Docente)
            .filter(Docente.id.in_(materia.docente_ids))
            .all()
        )

    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia


def update_materia(db: Session, materia_id: int, materia: MateriaCreate):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not db_materia:
        return None

    # 🔹 Campos simples
    if materia.nombre is not None:
        db_materia.nombre = materia.nombre

    if materia.codigo is not None:
        db_materia.codigo = materia.codigo

    # 🔹 CARRERAS (🔥 AQUÍ ESTABA EL PROBLEMA)
    if materia.carrera_ids is not None:
        carreras = (
            db.query(Carrera)
            .filter(Carrera.id.in_(materia.carrera_ids))
            .all()
        )
        db_materia.carreras = carreras

    # 🔹 DOCENTES
    if materia.docente_ids is not None:
        docentes = (
            db.query(Docente)
            .filter(Docente.id.in_(materia.docente_ids))
            .all()
        )
        db_materia.docentes = docentes

    # 🔹 SEDES (obligatorio)
    if materia.sede_ids is not None:
        sedes = (
            db.query(Sede)
            .filter(Sede.id.in_(materia.sede_ids))
            .all()
        )
        db_materia.sedes = sedes

    db.commit()
    db.refresh(db_materia)
    return db_materia

def delete_materia(db: Session, materia_id: int):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not db_materia:
        return False

    db.delete(db_materia)
    db.commit()
    return True
