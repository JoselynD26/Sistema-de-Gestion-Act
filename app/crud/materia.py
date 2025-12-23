from sqlalchemy.orm import Session
from app.models.materia import Materia
from app.models.sede import Sede
from app.schemas.materia import MateriaCreate

def get_materias(db: Session):
    return db.query(Materia).all()

def get_materias_por_sede(db: Session, sede_id: int):
    return db.query(Materia).join(Materia.sedes).filter(Sede.id == sede_id).all()

def get_materia(db: Session, materia_id: int):
    return db.query(Materia).filter(Materia.id == materia_id).first()

def create_materia(db: Session, materia: MateriaCreate):
    # Generar código si no se proporciona
    codigo = materia.codigo or f"MAT{db.query(Materia).count() + 1:03d}"
    
    db_materia = Materia(nombre=materia.nombre, codigo=codigo)
    
    # Agregar relaciones con sedes si se proporcionan
    if materia.sede_ids:
        sedes = db.query(Sede).filter(Sede.id.in_(materia.sede_ids)).all()
        db_materia.sedes = sedes
    
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

def update_materia(db: Session, materia_id: int, materia: MateriaCreate):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if db_materia:
        for key, value in materia.dict().items():
            setattr(db_materia, key, value)
        db.commit()
        db.refresh(db_materia)
    return db_materia

def delete_materia(db: Session, materia_id: int):
    db_materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if db_materia:
        db.delete(db_materia)
        db.commit()
        return True
    return False