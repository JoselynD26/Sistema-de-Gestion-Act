from sqlalchemy.orm import Session
from app.models.docente_vinculacion import DocenteVinculacion
from app.schemas.docente_vinculacion import DocenteVinculacionCreate

def crear_docente_vinculacion(db: Session, datos: DocenteVinculacionCreate):
    nuevo = DocenteVinculacion(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_docente_vinculaciones(db: Session):
    return db.query(DocenteVinculacion).all()

def eliminar_docente_vinculacion(db: Session, vinculacion_id: int):
    vinculo = db.query(DocenteVinculacion).get(vinculacion_id)
    if vinculo:
        db.delete(vinculo)
        db.commit()
    return vinculo