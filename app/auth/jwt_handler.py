from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

def crear_token(usuario_id: int, rol: str):
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    payload = {
        "sub": str(usuario_id),
        "rol": rol,
        "exp": expiracion
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token