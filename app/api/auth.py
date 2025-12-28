from fastapi import APIRouter, Depends, HTTPException
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
def solicitar_codigo_admin(email: str, nombres: str):
    from app.services.email_service import email_service

    try:
        success = email_service.send_admin_verification_email(email, nombres)
        if success:
            return {"message": "Código de verificación enviado al email"}
        else:
            raise HTTPException(status_code=500, detail="Error al enviar email")

    except Exception as e:
        print("ERROR solicitar_codigo_admin:", e)
        raise HTTPException(status_code=500, detail=str(e))


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
    import hashlib
    # Verificar contraseña actual
    if hashlib.sha256(datos.contrasena_actual.encode()).hexdigest() != usuario_actual.contrasena:
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
    
    # Actualizar contraseña
    usuario_actual.contrasena = hashlib.sha256(datos.nueva_contrasena.encode()).hexdigest()
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.post("/login/")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
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