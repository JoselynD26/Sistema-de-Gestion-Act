from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.usuario import Usuario

# 🔐 Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

# 🔑 Esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

# 🎟️ Generar token JWT
def crear_token(usuario_id: int, rol: str):
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    payload = {
        "sub": str(usuario_id),
        "rol": rol,
        "exp": expiracion
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# 👤 Obtener usuario desde el token
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: SessionLocal())):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
        rol = payload.get("rol")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# 🛡️ Verificar si el usuario es administrador
def solo_admin(usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")
    return usuario