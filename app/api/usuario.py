
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioResetPassword, UsuarioUpdate
from app.crud.usuario import (
    crear_usuario,
    autenticar_usuario,
    listar_usuarios,
    obtener_usuario,
    eliminar_usuario,
    crear_usuario_para_docente,
    docentes_sin_usuario,
    actualizar_usuario
)
from app.core.seguridad import obtener_usuario_actual, solo_admin, crear_token
from app.models.usuario import Usuario

router = APIRouter()

# Usamos get_db de core.config

# Crear usuario (solo admin)
@router.post("/", response_model=UsuarioOut, dependencies=[Depends(solo_admin)])
def registrar(data: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, data)

# Login y generación de token
@router.post("/login/")
def login(correo: str, contrasena: str, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, correo, contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token(usuario.id, usuario.rol)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario.correo,
        "rol": usuario.rol
    }

# Listar todos los usuarios (solo admin)
@router.get("/", response_model=list[UsuarioOut], dependencies=[Depends(solo_admin)])
def listar(db: Session = Depends(get_db)):
    return listar_usuarios(db)

# Obtener usuario por ID (solo admin)
@router.get("/{usuario_id}/", response_model=UsuarioOut, dependencies=[Depends(solo_admin)])
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    return obtener_usuario(db, usuario_id)

# Eliminar usuario (solo admin)
@router.delete("/{usuario_id}/", dependencies=[Depends(solo_admin)])
def eliminar(usuario_id: int, db: Session = Depends(get_db)):
    return eliminar_usuario(db, usuario_id)

# Crear cuenta para docente (solo admin)
@router.post("/docente/", response_model=UsuarioOut, dependencies=[Depends(solo_admin)])
def crear_para_docente(data: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario_para_docente(db, data)

# Listar docentes sin cuenta (solo admin)
@router.get("/docentes-sin-cuenta/", dependencies=[Depends(solo_admin)])
def listar_docentes_sin_usuario(db: Session = Depends(get_db)):
    return docentes_sin_usuario(db)

# Actualizar usuario (Universal: Admin a cualquiera, Docente a sí mismo)
@router.put("/{usuario_id}/", response_model=UsuarioOut)
@router.patch("/{usuario_id}/", response_model=UsuarioOut)
def update_usuario_universal(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    # Lógica de permisos similar al reset
    usuario_objetivo = None

    if usuario_actual.rol == "admin":
        usuario_objetivo = db.query(Usuario).get(usuario_id)
    else:
        # El usuario normal solo puede editarse a sí mismo (por ID usuario o ID docente)
        if usuario_id == usuario_actual.id or (usuario_actual.id_docente and usuario_id == usuario_actual.id_docente):
            usuario_objetivo = usuario_actual
        else:
            raise HTTPException(status_code=403, detail="No tienes permisos para editar este perfil")

    if not usuario_objetivo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Realizar la actualización
    for campo, valor in data.dict(exclude_unset=True).items():
        # Seguridad: Solo admin puede cambiar roles o id_docente de otros
        if usuario_actual.rol != "admin" and campo in ["rol", "id_docente"]:
            continue
        setattr(usuario_objetivo, campo, valor)
    
    db.commit()
    db.refresh(usuario_objetivo)
    return usuario_objetivo

# Ruta antigua para compatibilidad frontend (si la usan sin ID)
@router.put("/editar/", response_model=UsuarioOut)
def editar_mi_perfil_compat(
    data: UsuarioUpdate, 
    db: Session = Depends(get_db), 
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    return update_usuario_universal(usuario_actual.id, data, db, usuario_actual)

# Resetear contraseña (admin o el mismo usuario)
@router.put("/reset/{usuario_id}/")
def reset_contrasena(
    usuario_id: int, 
    data: UsuarioResetPassword, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    usuario_objetivo = None
    if usuario_actual.rol == "admin":
        usuario_objetivo = db.query(Usuario).get(usuario_id)
    else:
        if usuario_id == usuario_actual.id or (usuario_actual.id_docente and usuario_id == usuario_actual.id_docente):
            usuario_objetivo = usuario_actual
        else:
            raise HTTPException(status_code=403, detail="No tienes permisos para resetear esta contraseña")

    if not usuario_objetivo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    from app.core.seguridad import obtener_hash_contrasena
    usuario_objetivo.contrasena = obtener_hash_contrasena(data.nueva_contrasena)
    db.commit()
    return {"message": "Contraseña reseteada exitosamente"}

# Endpoint alias para recuperación (Compatibilidad con Frontend)
from app.schemas.usuario import UsuarioCreate # Dummy import if needed, or use Body
from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    correo: EmailStr

@router.post("/recuperar-contrasena/")
def recuperar_contrasena_alias(request: EmailRequest, db: Session = Depends(get_db)):
    """
    Alias para solicitar recuperación de contraseña.
    Redirige lógica a la misma implementación que auth.solicitar_recuperacion
    """
    from app.services.email_service import email_service
    from app.core.seguridad import obtener_hash_contrasena
    import secrets
    import string
    from fastapi import HTTPException

    # Lógica duplicada de auth.py (Idealmente refactorizar a controlador común, pero por rapidez duplicamos aquí)
    usuario = db.query(Usuario).filter(Usuario.correo == request.correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    usuario.contrasena = obtener_hash_contrasena(temp_password)
    db.commit()

    nombre_email = usuario.nombres if usuario.nombres else "Usuario"
    success = email_service.send_password_recovery_email(request.correo, temp_password, nombre_email)
    
    if not success:
         raise HTTPException(status_code=500, detail="Error enviando el correo")
         
    return {"message": "Correo de recuperación enviado exitosamente"}


