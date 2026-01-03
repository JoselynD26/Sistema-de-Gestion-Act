from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioChangePassword
from app.crud.usuario import crear_usuario, autenticar_usuario
from app.core.config import SessionLocal
from app.core.seguridad import crear_token, obtener_usuario_actual
from app.models.usuario import Usuario
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/solicitar-codigo-admin/")
def solicitar_codigo_admin(email: str, nombres: str, background_tasks: BackgroundTasks):
    from app.services.email_service import email_service
    print(f"DEBUG: solicitud codigo admin para {email} ({nombres})")
    try:
        background_tasks.add_task(email_service.send_admin_verification_email, email, nombres)
        return {"message": "Si hay administradores en el sistema, se les enviará un código de verificación."}
    except Exception as e:
        print(f"ERROR solicitar_codigo_admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class EmailRequest(BaseModel):
    correo: EmailStr

@router.post("/solicitar-recuperacion/")
def solicitar_recuperacion(request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Solicita recuperación de contraseña:
    1. Verifica que el correo exista
    2. Genera una contraseña temporal
    3. Actualiza el usuario con la nueva contraseña
    4. Envía la contraseña por correo (via BackgroundTasks)
    """
    from app.services.email_service import email_service
    from app.core.seguridad import obtener_hash_contrasena
    import secrets
    import string

    # 1. Buscar usuario
    usuario = db.query(Usuario).filter(Usuario.correo == request.correo).first()
    if not usuario:
        print(f"DEBUG ALERT: Se intento recuperar contrasena para correo NO REGISTRADO: {request.correo}")
        raise HTTPException(status_code=404, detail=f"El correo {request.correo} no está registrado en el sistema.")

    # 2. Generar contraseña temporal segura
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    # 3. Actualizar contraseña en BD
    hashed_password = obtener_hash_contrasena(temp_password)
    usuario.contrasena = hashed_password
    db.commit()

    # 4. Enviar correo via BackgroundTasks
    print(f"DEBUG: solicitud recuperacion para {request.correo}, pass temporal generada")
    try:
        nombre_email = usuario.nombres if usuario.nombres else "Usuario"
        
        background_tasks.add_task(
            email_service.send_password_recovery_email,
            request.correo,
            temp_password,
            nombre_email
        )
        
        return {"message": "Correo de recuperación solicitado exitosamente"}
        
    except Exception as e:
        print(f"Error en solicitar_recuperacion (envio correo): {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")



@router.post("/registro-admin/")
def registrar_admin(
    correo: str,
    contrasena: str, 
    nombres: str,
    apellidos: str,
    codigo_verificacion: str,
    db: Session = Depends(get_db)
):
    """Registra admin solo con código de verificación válido"""
    from app.services.email_service import email_service
    
    # Verificar código
    if not email_service.verify_code(correo, codigo_verificacion):
        raise HTTPException(status_code=400, detail="Código de verificación inválido o expirado")
    
    # Crear usuario admin
    from app.schemas.usuario import UsuarioCreate
    usuario_data = UsuarioCreate(
        correo=correo,
        contrasena=contrasena,
        nombres=nombres,
        apellidos=apellidos,
        rol="admin"
    )
    
    return crear_usuario(db, usuario_data)

@router.put("/cambiar-contrasena/")
def cambiar_contrasena(
    datos: UsuarioChangePassword,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    # Validar espacios en nueva contraseña
    if " " in datos.nueva_contrasena:
        raise HTTPException(status_code=400, detail="La nueva contraseña no puede contener espacios")

    from app.core.seguridad import obtener_hash_contrasena, verificar_contrasena
    # Verificar contraseña actual
    if not verificar_contrasena(datos.contrasena_actual, usuario_actual.contrasena):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
    
    # Actualizar contraseña
    usuario_actual.contrasena = obtener_hash_contrasena(datos.nueva_contrasena)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.post("/login/")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    # Validar espacios
    if " " in datos.correo or " " in datos.contrasena:
        raise HTTPException(status_code=400, detail="El correo y la contraseña no pueden contener espacios")

    usuario = autenticar_usuario(db, datos.correo, datos.contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token(usuario.id, usuario.rol)
    
    response = {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellidos": usuario.apellidos
    }
    
    # Si es docente, agregar el docente_id y obtener nombres del registro de docente
    if usuario.rol == "docente" and usuario.id_docente:
        response["docente_id"] = usuario.id_docente
        
        # Obtener nombres del registro de docente si el usuario no los tiene
        if not usuario.nombres or not usuario.apellidos:
            from app.models.docente import Docente
            docente = db.query(Docente).filter(Docente.id == usuario.id_docente).first()
            if docente:
                response["nombres"] = docente.nombres
                response["apellidos"] = docente.apellidos
    
    print(f"DEBUG LOGIN - Usuario: {response.get('nombres')} {response.get('apellidos')}, Rol: {usuario.rol}")
    
    return response