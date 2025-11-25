from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import SessionLocal
from app.models.usuario import Usuario
from fastapi.security import OAuth2PasswordBearer

# Configuración del esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Clave secreta y algoritmo (debes usar los mismos que en tu login)
SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"

# Conexión a la base
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener usuario desde el token JWT
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: int = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Protección por rol
def verificar_rol(rol_requerido: str):
    def wrapper(usuario: Usuario = Depends(obtener_usuario_actual)):
        if usuario.rol != rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso restringido para rol: {usuario.rol}"
            )
        return usuario
    return wrapper