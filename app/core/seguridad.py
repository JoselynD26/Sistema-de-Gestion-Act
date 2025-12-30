from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.usuario import Usuario

from passlib.context import CryptContext
import hashlib

# 🔐 Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

# Configuración de hashing de contraseñas
# Usamos argon2 como preferido, pero bcrypt también es una buena opción standard
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# 🔑 Esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def obtener_hash_contrasena(contrasena: str) -> str:
    """Genera un hash seguro para la contraseña."""
    return pwd_context.hash(contrasena)

def verificar_contrasena(contrasena_plana: str, contrasena_hashed: str) -> bool:
    """
    Verifica la contraseña soportando:
    1. Hashes modernos (Argon2/Bcrypt) vía passlib.
    2. Hashes legacy (SHA256) vía hashlib (para compatibilidad).
    """
    try:
        # Intenta verificar con passlib (maneja argon2/bcrypt automáticamente)
        if pwd_context.verify(contrasena_plana, contrasena_hashed):
            return True
    except Exception:
        # Si falla (formato desconocido), podría ser legacy
        pass

    # Verificación fallback para SHA256 (Legacy)
    # Supabase/Código anterior usaba: hashlib.sha256(pwd.encode()).hexdigest()
    try:
        hash_legacy = hashlib.sha256(contrasena_plana.encode()).hexdigest()
        if hash_legacy == contrasena_hashed:
            # TODO: Aquí podríamos implementar "rehash" automático para migrar al usuario
            return True
    except Exception:
        pass
        
    return False

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