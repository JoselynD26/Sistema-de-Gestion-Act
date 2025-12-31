from sqlalchemy.orm import Session
from app.models import Curso, Sede, Aula, Horario, CursoAula, CursoHorario, Materia, Docente
# from app.models.materia_carrera import MateriaCarrera # Eliminado
# from app.models.docente_materia import DocenteMateria # Eliminado
# Sirve para obtener una vista de cursos con sus detalles y vinculaciones
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
        # Asumiendo que Curso tiene relación 'carrera' y Carrera tiene relación 'materias'
        # O si Curso tiene relación directa 'materias' (lo cual es menos común, usualmente es por carrera/malla)
        # Revisando el código anterior: MateriaCarrera.id_carrera == c.id_carrera
        # Esto sugiere que se buscaban las materias de la carrera del curso.

        materias_nombres = []
        if c.carrera: # Si existe la relación
             materias_nombres = [m.nombre for m in c.carrera.materias]
        else:
            # Fallback si no hay relación ORM cargada o definida, pero intentamos evitar el join manual con tabla borrada
            # Si Carrera es un modelo y tiene 'materias' definido (como vimos en Docente), esto debería funcionar.
             pass

        # Docentes que dan esas materias
        # Anteriormente: DocenteMateria filtrado por todas las materias?
        # .filter(DocenteMateria.id_materia.in_([m.id_materia for m in db.query(Materia).all()]))
        # Eso filtraba por TODAS las materias de la DB? Eso parece un bug del código original o una lógica extraña.
        # Asumiremos que quiere docentes de las materias DEL CURSO.
        
        docentes_set = set()
        if c.carrera:
            for materia in c.carrera.materias:
                for docente in materia.docentes:
                     docentes_set.add(f"{docente.nombres} {docente.apellidos}")
        
        resultado.append({
            "id_curso": c.id_curso,
            "nivel": c.nivel,
            "paralelo": c.paralelo,
            "jornada": c.jornada,
            "materias": materias_nombres,
            "docentes": list(docentes_set)
        })

    return resultado