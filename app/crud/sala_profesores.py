from sqlalchemy.orm import Session
from app.models.sala_profesores import SalaProfesores
from app.schemas.sala_profesores import SalaProfesoresCreate

def crear_sala(db: Session, data: SalaProfesoresCreate):
    nueva = SalaProfesores(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_salas(db: Session):
    return db.query(SalaProfesores).all()

def listar_salas_por_sede(db: Session, sede_id: int):
    return db.query(SalaProfesores).filter(SalaProfesores.sede_id == sede_id).all()

def actualizar_sala(db: Session, sala_id: int, data: SalaProfesoresCreate):
    sala = db.query(SalaProfesores).filter(SalaProfesores.id == sala_id).first()
    if not sala:
        return None
    
    for campo, valor in data.dict().items():
        setattr(sala, campo, valor)
    
    db.commit()
    db.refresh(sala)
    return sala

def eliminar_sala(db: Session, sala_id: int):
    sala = db.query(SalaProfesores).filter(SalaProfesores.id == sala_id).first()
    if not sala:
        return None
    
    db.delete(sala)
    db.commit()
    return sala