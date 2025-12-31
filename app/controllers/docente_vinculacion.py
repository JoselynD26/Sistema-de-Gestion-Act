from sqlalchemy.orm import Session
from app.models.docente import Docente
from app.models.carrera import Carrera
from app.models.materia import Materia
from app.models.aula import Aula
from app.models.escritorio import Escritorio
from app.models.docente_sala import DocenteSala
# from app.models.docente_carrera import DocenteCarrera # Eliminado
# from app.models.docente_materia import DocenteMateria # Eliminado

# Sirve para obtener una vista de docentes con sus vinculaciones
def vista_docentes_con_vinculaciones(db: Session):
    docentes = db.query(Docente).all()
    resultado = []

    for d in docentes:
        # Usando las relaciones definidas en el modelo Docente (Many-to-Many)
        carreras = [c.nombre for c in d.carreras]
        materias = [m.nombre for m in d.materias]

        # Para Salas, si DocenteSala es un modelo intermedio explícito sin relationship en Docente:
        # Verificamos si podemos usar relationship o mantenemos la query manual con DocenteSala.
        # Asumiendo que DocenteSala aún existe (no fue borrado en pasos anteriores).
        salas = (
            db.query(Aula.nombre)
            .join(DocenteSala, Aula.id == DocenteSala.id_aula)
            .filter(DocenteSala.id_docente == d.id)
            .all()
        )

        escritorios = (
            db.query(Escritorio.codigo)
            .filter(Escritorio.id_docente == d.id) # Corrección de id_docente a id si fuera necesario, pero Escritorio suele tener FK id_docente.
            .all()
        )

        resultado.append({
            "id_docente": d.id,
            "nombres": d.nombres,
            "apellidos": d.apellidos,
            "carreras": carreras,
            "materias": materias,
            "salas": [s[0] for s in salas],
            "escritorios": [e[0] for e in escritorios]
        })

    return resultado