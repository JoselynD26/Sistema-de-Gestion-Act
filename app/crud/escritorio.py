from sqlalchemy.orm import Session, joinedload
from app.models.escritorio import Escritorio
from app.schemas.escritorio import EscritorioCreate, EscritorioUpdate
from app.models.sala import Sala
from app.models.sede import Sede
from app.models.carrera import Carrera
from app.models.docente import Docente

# ======================================
#   CREAR ESCRITORIO
# ======================================
def crear_escritorio(db: Session, datos: EscritorioCreate):
    nuevo = Escritorio(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ======================================
#   LISTAR ESCRITORIOS POR SEDE
# ======================================
from sqlalchemy.orm import joinedload

def listar_escritorios_por_sede(db: Session, id_sede: int):
    escritorios = (
        db.query(Escritorio)
        .join(Sala, Escritorio.sala_id == Sala.id)
        .filter(Sala.sede_id == id_sede)
        .options(
            joinedload(Escritorio.sala),
            joinedload(Escritorio.carrera),
            joinedload(Escritorio.docente),
        )
        .all()
    )

    resultado = []
    for e in escritorios:
        resultado.append({
            "id": e.id,
            "codigo": e.codigo,
            "estado": e.estado,
            "jornada": e.jornada,
            "sala_id": e.sala_id,
            "sala_nombre": e.sala.nombre if e.sala else None,
            "carrera_id": e.carrera_id,
            "carrera_nombre": e.carrera.nombre if e.carrera else None,
            "docente_id": e.docente_id,
            "docente_nombre": f"{e.docente.nombres} {e.docente.apellidos}" if e.docente else None,
        })
    return resultado

# ======================================
#   LISTAR TODOS
# ======================================
def listar_escritorios(db: Session):
    escritorios = (
        db.query(Escritorio)
        .options(
            joinedload(Escritorio.sala),
            joinedload(Escritorio.carrera),
            joinedload(Escritorio.docente),
        )
        .all()
    )

    resultado = []
    for e in escritorios:
        resultado.append({
            "id": e.id,
            "codigo": e.codigo,
            "estado": e.estado,
            "jornada": e.jornada,
            "sala_id": e.sala_id,
            "sala_nombre": e.sala.nombre if e.sala else None,
            "carrera_id": e.carrera_id,
            "carrera_nombre": e.carrera.nombre if e.carrera else None,
            "docente_id": e.docente_id,
            "docente_nombre": f"{e.docente.nombres} {e.docente.apellidos}" if e.docente else None,
        })
    return resultado

# ======================================
#   FILTROS
# ======================================
def listar_escritorios_por_sala(db: Session, sala_id: int):
    return db.query(Escritorio).filter_by(sala_id=sala_id).all()

def listar_escritorios_por_carrera(db: Session, carrera_id: int):
    return db.query(Escritorio).filter_by(carrera_id=carrera_id).all()

# ======================================
#   OBTENER / ELIMINAR
# ======================================
def obtener_escritorio(db: Session, escritorio_id: int):
    return db.query(Escritorio).get(escritorio_id)

def eliminar_escritorio(db: Session, escritorio_id: int):
    esc = db.query(Escritorio).get(escritorio_id)
    if esc:
        db.delete(esc)
        db.commit()
    return esc

# ======================================
#   ASIGNAR DOCENTE
# ======================================
def asignar_docente_a_escritorio(db: Session, escritorio_id: int, docente_id: int):
    esc = db.query(Escritorio).get(escritorio_id)
    if not esc:
        return None
    esc.docente_id = docente_id
    db.commit()
    db.refresh(esc)
    return esc

# ======================================
#   ACTUALIZAR ESCRITORIO
# ======================================
def actualizar_escritorio(db: Session, escritorio_id: int, data: EscritorioUpdate):
    esc = db.query(Escritorio).filter(Escritorio.id == escritorio_id).first()
    if not esc:
        return None

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(esc, campo, valor)

    db.commit()
    db.refresh(esc)
    return esc