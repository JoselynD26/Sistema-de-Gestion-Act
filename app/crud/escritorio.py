from sqlalchemy.orm import Session, joinedload
from app.models.escritorio import Escritorio
from app.schemas.escritorio import EscritorioCreate, EscritorioUpdate
from app.models.sala_profesores import SalaProfesores
from app.models.sede import Sede
from app.models.carrera import Carrera
from app.models.docente import Docente

# ======================================
#   CREAR ESCRITORIO
# ======================================
def crear_escritorio(db: Session, datos: EscritorioCreate):
    # Verificar que la sala existe
    sala = db.query(SalaProfesores).filter(SalaProfesores.id == datos.sala_id).first()
    if not sala:
        raise ValueError(f"La sala con ID {datos.sala_id} no existe")
    
    # Verificar que la carrera existe
    carrera = db.query(Carrera).filter(Carrera.id == datos.carrera_id).first()
    if not carrera:
        raise ValueError(f"La carrera con ID {datos.carrera_id} no existe")
    
    # Verificar que el docente existe (si se proporciona)
    if datos.docente_id:
        docente = db.query(Docente).filter(Docente.id == datos.docente_id).first()
        if not docente:
            raise ValueError(f"El docente con ID {datos.docente_id} no existe")
    
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
    try:
        escritorios = (
            db.query(Escritorio)
            .join(SalaProfesores, Escritorio.sala_id == SalaProfesores.id)
            .filter(SalaProfesores.sede_id == id_sede)
            .all()
        )

        resultado = []
        for e in escritorios:
            # Obtener sala manualmente
            sala = db.query(SalaProfesores).filter(SalaProfesores.id == e.sala_id).first()
            # Obtener carrera manualmente
            carrera = db.query(Carrera).filter(Carrera.id == e.carrera_id).first()
            # Obtener docente manualmente
            docente = db.query(Docente).filter(Docente.id == e.docente_id).first() if e.docente_id else None
            
            resultado.append({
                "id": e.id,
                "codigo": e.codigo,
                "estado": e.estado,
                "jornada": e.jornada,
                "sala_id": e.sala_id,
                "sala_nombre": sala.nombre if sala else None,
                "carrera_id": e.carrera_id,
                "carrera_nombre": carrera.nombre if carrera else None,
                "docente_id": e.docente_id,
                "docente_nombre": f"{docente.nombres} {docente.apellidos}" if docente else None,
            })
        return resultado
    except Exception as e:
        print(f"Error en listar_escritorios_por_sede: {e}")
        return []

# ======================================
#   LISTAR TODOS
# ======================================
def listar_escritorios(db: Session):
    try:
        escritorios = db.query(Escritorio).all()
        resultado = []
        
        for e in escritorios:
            # Obtener sala manualmente
            sala = db.query(SalaProfesores).filter(SalaProfesores.id == e.sala_id).first()
            # Obtener carrera manualmente
            carrera = db.query(Carrera).filter(Carrera.id == e.carrera_id).first()
            # Obtener docente manualmente
            docente = db.query(Docente).filter(Docente.id == e.docente_id).first() if e.docente_id else None
            
            resultado.append({
                "id": e.id,
                "codigo": e.codigo,
                "estado": e.estado,
                "jornada": e.jornada,
                "sala_id": e.sala_id,
                "sala_nombre": sala.nombre if sala else None,
                "carrera_id": e.carrera_id,
                "carrera_nombre": carrera.nombre if carrera else None,
                "docente_id": e.docente_id,
                "docente_nombre": f"{docente.nombres} {docente.apellidos}" if docente else None,
            })
        return resultado
    except Exception as e:
        print(f"Error en listar_escritorios: {e}")
        return []

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