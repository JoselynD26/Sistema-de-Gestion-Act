from sqlalchemy.orm import Session
from app.models import Curso, Sede, Aula, Horario, CursoAula, CursoHorario, Materia, Docente
from app.models.materia_carrera import MateriaCarrera
from app.models.docente_materia import DocenteMateria

def vista_cursos_con_detalle(db: Session):
    cursos = db.query(Curso).all()
    resultado = []

    for c in cursos:
        sede = db.query(Sede.nombre).filter(Sede.id_sede == c.id_sede).first()
        aulas = (
            db.query(Aula.nombre)
            .join(CursoAula, Aula.id_aula == CursoAula.id_aula)
            .filter(CursoAula.id_curso == c.id_curso)
            .all()
        )
        horarios = (
            db.query(Horario)
            .join(CursoHorario, Horario.id_horario == CursoHorario.id_horario)
            .filter(CursoHorario.id_curso == c.id_curso)
            .all()
        )

        horarios_detalle = []
        for h in horarios:
            materia = db.query(Materia.nombre).filter(Materia.id_materia == h.id_materia).first()
            docente = db.query(Docente.nombres, Docente.apellidos).filter(Docente.id_docente == h.id_docente).first()
            estado = h.estado

            horarios_detalle.append({
                "bloque": getattr(h, "bloque", None),
                "materia": materia[0] if materia else None,
                "docente": f"{docente[0]} {docente[1]}" if docente else None,
                "estado": estado
            })

        resultado.append({
            "id_curso": c.id_curso,
            "nivel": c.nivel,
            "paralelo": c.paralelo,
            "jornada": c.jornada,
            "sede": sede[0] if sede else None,
            "aulas": [a[0] for a in aulas],
            "horarios": horarios_detalle
        })

    return resultado

def vista_cursos_con_vinculaciones(db: Session):
    cursos = db.query(Curso).all()
    resultado = []

    for c in cursos:
        materias = (
            db.query(Materia.nombre)
            .join(MateriaCarrera, Materia.id_materia == MateriaCarrera.id_materia)
            .filter(MateriaCarrera.id_carrera == c.id_carrera)
            .all()
        )
        docentes = (
            db.query(Docente.nombres, Docente.apellidos)
            .join(DocenteMateria, Docente.id_docente == DocenteMateria.id_docente)
            .filter(DocenteMateria.id_materia.in_([m.id_materia for m in db.query(Materia).all()]))
            .all()
        )

        resultado.append({
            "id_curso": c.id_curso,
            "nivel": c.nivel,
            "paralelo": c.paralelo,
            "jornada": c.jornada,
            "materias": [m[0] for m in materias],
            "docentes": [f"{d[0]} {d[1]}" for d in docentes]
        })

    return resultado