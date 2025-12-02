from sqlalchemy.orm import Session
from app.models.horario import Horario
from datetime import date
# Sirve para obtener los horarios cancelados por sede y fecha
def horarios_cancelados(db: Session, sede_id: int, fecha: date):
    return db.query(Horario).filter_by(
        id_sede=sede_id,
        fecha=fecha,
        estado="cancelado"
    ).all()