from app.core.config import SessionLocal
from app.crud import docente as crud_docente
from app.schemas.docente import DocenteCreate, Regimen, Observacion
from app.models.sede import Sede
from app.models.docente import Docente
from sqlalchemy.orm import Session
import traceback

def test():
    db = SessionLocal()
    try:
        # Get a valid sede
        sede = db.query(Sede).first()
        if not sede:
            print("No sedes found! Cannot create docente safely without a Sede.")
            # Verify if we can create one or just exit
            return

        print(f"Using Sede ID: {sede.id}")

        # Clean up if exists
        cedula_test = "9999999999"
        existing = db.query(Docente).filter(Docente.cedula == cedula_test).first()
        if existing:
            print("Deleting existing test docente...")
            db.delete(existing)
            db.commit()

        # Create dummy docente data
        data = DocenteCreate(
            cedula=cedula_test,
            correo="test_docente_debug@yavirac.edu.ec",
            apellidos="TestDebug",
            nombres="DocenteDebug",
            regimen=Regimen.codigo, # "Codigo de trabajo"
            observacion=Observacion.completo, # "Tiempo completo"
            sede_id=sede.id
        )

        print("Attempting to create docente via crud...")
        nuevo = crud_docente.crear_docente(db, data)
        print(f"SUCCESS: Created Docente ID: {nuevo.id}, Cedula: {nuevo.cedula}")

        # Clean up
        db.delete(nuevo)
        db.commit()
        print("Test docente deleted.")

    except Exception as e:
        print("FAILED to create docente.")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test()
