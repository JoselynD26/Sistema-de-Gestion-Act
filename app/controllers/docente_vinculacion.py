from sqlalchemy.orm import Session
from app.models.docente import Docente
from app.models.carrera import Carrera
from app.models.materia import Materia
from app.models.aula import Aula
from app.models.escritorio import Escritorio
from app.models.docente_carrera import DocenteCarrera
from app.models.docente_materia import DocenteMateria
from app.models.docente_sala import DocenteSala

def vista_docentes_con_vinculaciones(db: Session):
    docentes = db.query(Docente).all()
    resultado = []

    for d in docentes:
        carreras = (
            db.query(Carrera.nombre)
            .join(DocenteCarrera, Carrera.id_carrera == DocenteCarrera.id_carrera)
            .filter(DocenteCarrera.id_docente == d.id_docente)
            .all()
        )
        materias = (
            db.query(Materia.nombre)
            .join(DocenteMateria, Materia.id_materia == DocenteMateria.id_materia)
            .filter(DocenteMateria.id_docente == d.id_docente)
            .all()
        )
        salas = (
            db.query(Aula.nombre)
            .join(DocenteSala, Aula.id_aula == DocenteSala.id_aula)
            .filter(DocenteSala.id_docente == d.id_docente)
            .all()
        )
        escritorios = (
            db.query(Escritorio.codigo)
            .filter(Escritorio.id_docente == d.id_docente)
            .all()
        )

        resultado.append({
            "id_docente": d.id_docente,
            "nombres": d.nombres,
            "apellidos": d.apellidos,
            "carreras": [c[0] for c in carreras],
            "materias": [m[0] for m in materias],
            "salas": [s[0] for s in salas],
            "escritorios": [e[0] for e in escritorios]
        })

    return resultado