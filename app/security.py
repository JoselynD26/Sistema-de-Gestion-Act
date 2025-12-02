from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta y algoritmo (usa la misma que en tu login)
SECRET_KEY = "TU_CLAVE_SECRETA"   # ⚠️ cámbiala por una clave segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

# -------------------
# Manejo de contraseñas
# -------------------
def hash_contrasena(password: str) -> str:
    """Genera el hash de una contraseña en texto plano."""
    return pwd_context.hash(password)

def verificar_contrasena(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

# -------------------
# Manejo de JWT
# -------------------
def crear_token(usuario_id: int) -> str:
    """Crea un JWT válido para el usuario."""
    datos = {
        "sub": str(usuario_id),
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    """Decodifica un JWT y devuelve el payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None