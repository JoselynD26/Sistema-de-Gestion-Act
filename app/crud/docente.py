from sqlalchemy.orm import Session
from app.models.docente import Docente
from app.schemas.docente import DocenteCreate


def crear_docente(db: Session, datos: DocenteCreate):
    """
    Crea un docente y lo asocia correctamente a una sede
    """
    nuevo = Docente(
        cedula=datos.cedula,
        correo=datos.correo,
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        regimen=datos.regimen,
        observacion=datos.observacion,
        sede_id=datos.sede_id,  # 🔥 CLAVE: asociación correcta
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_docentes(db: Session):
    """
    Lista todos los docentes
    """
    return db.query(Docente).all()


def listar_docentes_por_sede(db: Session, id_sede: int):
    """
    Lista docentes filtrados por sede
    """
    return (
        db.query(Docente)
        .filter(Docente.sede_id == id_sede)
        .order_by(Docente.apellidos, Docente.nombres)
        .all()
    )


def obtener_docente(db: Session, docente_id: int):
    """
    Obtiene un docente por ID
    """
    return db.query(Docente).filter(Docente.id == docente_id).first()


def actualizar_docente(db: Session, id_docente: int, docente_data: DocenteCreate):
    """
    Actualiza los datos de un docente
    """
    docente = db.query(Docente).filter(Docente.id == id_docente).first()
    if not docente:
        return None

    datos = docente_data.dict(exclude_unset=True)

    for key, value in datos.items():
        setattr(docente, key, value)

    db.commit()
    db.refresh(docente)
    return docente


def eliminar_docente(db: Session, docente_id: int):
    """
    Elimina un docente
    """
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        return None

    db.delete(docente)
    db.commit()
    return docente
