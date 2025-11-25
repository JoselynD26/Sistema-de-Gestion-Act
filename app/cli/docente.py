import typer
from app.core.config import SessionLocal
from app.schemas.docente import DocenteCreate, Regimen, Observacion
from app.crud.docente import crear_docente

app = typer.Typer()

@app.command()
def registrar(
    cedula: str,
    correo: str,
    apellidos: str,
    nombres: str,
    regimen: Regimen,
    observacion: Observacion
):
    db = SessionLocal()
    docente = DocenteCreate(
        cedula=cedula,
        correo=correo,
        apellidos=apellidos,
        nombres=nombres,
        regimen=regimen,
        observacion=observacion
    )
    creado = crear_docente(db, docente)
    typer.echo(f"Docente registrado: {creado.nombres} {creado.apellidos}")