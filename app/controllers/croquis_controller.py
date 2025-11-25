from sqlalchemy.orm import Session
from app.models import Sala, Escritorio, Docente, Carrera

def croquis_por_sala(db: Session, sala_id: int):
    sala = db.query(Sala).get(sala_id)
    if not sala:
        return None

    escritorios = db.query(Escritorio).filter_by(id_sala=sala_id).all()
    croquis = {}

    for esc in escritorios:
        carrera = db.query(Carrera).get(esc.id_carrera)
        docente = db.query(Docente).get(esc.id_docente) if esc.id_docente else None

        seccion = carrera.nombre if carrera else "Sin carrera"
        if seccion not in croquis:
            croquis[seccion] = []

        croquis[seccion].append({
            "escritorio_id": esc.id,
            "codigo": esc.codigo,
            "docente": f"{docente.nombres} {docente.apellidos}" if docente else "Disponible"
        })

    return {
        "sala": sala.nombre,
        "jornada": sala.jornada,
        "tipo": sala.tipo,
        "secciones": croquis
    }

def croquis_por_sede(db: Session, sede_id: int):
    salas = db.query(Sala).filter_by(id_sede=sede_id).all()
    resultado = []

    for sala in salas:
        escritorios = db.query(Escritorio).filter_by(id_sala=sala.id).all()
        secciones = {}

        for esc in escritorios:
            carrera = db.query(Carrera).get(esc.id_carrera)
            docente = db.query(Docente).get(esc.id_docente) if esc.id_docente else None

            nombre_carrera = carrera.nombre if carrera else "Sin carrera"
            if nombre_carrera not in secciones:
                secciones[nombre_carrera] = []

            secciones[nombre_carrera].append({
                "escritorio_id": esc.id,
                "codigo": esc.codigo,
                "docente": f"{docente.nombres} {docente.apellidos}" if docente else "Disponible"
            })

        resultado.append({
            "sala_id": sala.id,
            "nombre": sala.nombre,
            "jornada": sala.jornada,
            "tipo": sala.tipo,
            "secciones": secciones
        })

    return {
        "sede_id": sede_id,
        "salas": resultado
    }

def croquis_por_sede_filtrado(db: Session, sede_id: int, jornada: str, carrera_id: int):
    salas = db.query(Sala).filter_by(id_sede=sede_id, jornada=jornada).all()
    resultado = []

    for sala in salas:
        escritorios = db.query(Escritorio).filter_by(id_sala=sala.id, id_carrera=carrera_id).all()
        secciones = {}

        carrera = db.query(Carrera).get(carrera_id)
        nombre_carrera = carrera.nombre if carrera else "Sin carrera"
        secciones[nombre_carrera] = []

        for esc in escritorios:
            docente = db.query(Docente).get(esc.id_docente) if esc.id_docente else None
            secciones[nombre_carrera].append({
                "escritorio_id": esc.id,
                "codigo": esc.codigo,
                "docente": f"{docente.nombres} {docente.apellidos}" if docente else "Disponible"
            })

        resultado.append({
            "sala_id": sala.id,
            "nombre": sala.nombre,
            "jornada": sala.jornada,
            "tipo": sala.tipo,
            "secciones": secciones
        })

    return {
        "sede_id": sede_id,
        "jornada": jornada,
        "carrera_id": carrera_id,
        "salas": resultado
    }