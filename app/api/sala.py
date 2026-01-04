from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.schemas.sala import SalaCreate, SalaOut
from app.crud import sala as crud
from app.core.seguridad import verificar_rol
from app.dependencies.permisos import verificar_permiso_db

router = APIRouter()

# -------------------
# Dependencia para obtener la sesión de BD
# -------------------

# -------------------
# Endpoints principales (CRUD)
# -------------------

@router.post("/", response_model=SalaOut)
def crear_sala(data: SalaCreate, db: Session = Depends(get_db)):
    return crud.crear_sala(db, data)

@router.get("/sede/{sede_id}")
def listar_salas_por_sede(sede_id: int, db: Session = Depends(get_db)):
    return crud.listar_salas_por_sede(db, sede_id)

@router.get("/{sala_id}")
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    return crud.obtener_sala(db, sala_id)

@router.put("/{sala_id}", response_model=SalaOut)
def actualizar_sala(sala_id: int, data: SalaCreate, db: Session = Depends(get_db)):
    return crud.actualizar_sala(db, sala_id, data)

@router.delete("/{sala_id}")
def eliminar_sala(sala_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_sala(db, sala_id)

# -------------------
# Endpoints protegidos (roles/permisos)
# -------------------

@router.post("/roles/")
def crear_sala_por_rol(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verificar_rol("admin"))  # ✅ uso correcto de verificar_rol
):
    # Aquí iría la lógica de creación con roles
    return {"msg": f"Sala creada por usuario {usuario_id} con rol admin"}

@router.post("/permisos/")
def crear_sala_por_permiso(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verificar_permiso_db("crear_sala"))
):
    # Aquí iría la lógica de creación con permisos
    return {"msg": f"Sala creada por usuario {usuario_id} con permiso crear_sala"}