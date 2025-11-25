from sqlalchemy.orm import Session
from app.models.plaza import Plaza
from app.schemas.plaza import PlazaCreate

def crear_plaza(db: Session, datos: PlazaCreate):
    nueva = Plaza(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva