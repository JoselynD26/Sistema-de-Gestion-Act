from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.models.permiso import Permiso

def vista_roles_con_permisos(db: Session):
    roles = db.query(Rol).filter(Rol.nombre.in_(["admin", "docente"])).all()
    resultado = []

    for rol in roles:
        permisos = db.query(Permiso).filter_by(id_rol=rol.id).all()
        acciones = [p.accion for p in permisos]

        resultado.append({
            "rol_id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": acciones
        })

    return resultado