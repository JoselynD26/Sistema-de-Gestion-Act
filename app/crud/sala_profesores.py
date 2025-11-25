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