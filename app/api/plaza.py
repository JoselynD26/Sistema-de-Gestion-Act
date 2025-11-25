from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.plaza import PlazaCreate
from app.crud.plaza import crear_plaza

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/plazas/")
def crear_plaza_endpoint(plaza: PlazaCreate, db: Session = Depends(get_db)):
    return crear_plaza(db, plaza)