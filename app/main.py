from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Importación de rutas
from app.api import (
    docente, aula, materia, reserva,
    carrera, curso, horario, plaza, sede, sala_profesores, escritorio,
    materia_carrera, sala_carrera, curso_aula, curso_horario,
    docente_materia, docente_carrera, auth, docente_vinculacion,
    usuario, usuario_rol, rol, permiso, rol_permiso,
    notificacion, croquis, curso_vinculacion, panel_inicio
)

app = FastAPI(
    title="Sistema Académico",
    description="API protegida con JWT por rol",
    version="1.0.0"
)

# Seguridad global para Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas principales
app.include_router(docente.router)
app.include_router(aula.router)
app.include_router(materia.router)
app.include_router(reserva.router)
app.include_router(carrera.router)
app.include_router(curso.router)
app.include_router(horario.router)
app.include_router(plaza.router)
app.include_router(sede.router)
app.include_router(sala_profesores.router)
app.include_router(escritorio.router)
app.include_router(materia_carrera.router)
app.include_router(sala_carrera.router)
app.include_router(curso_aula.router)
app.include_router(curso_horario.router)
app.include_router(docente_materia.router)
app.include_router(docente_carrera.router)
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(usuario_rol.router)
app.include_router(rol.router)
app.include_router(permiso.router)
app.include_router(rol_permiso.router)
app.include_router(notificacion.router)
app.include_router(croquis.router)
app.include_router(curso_vinculacion.router)
app.include_router(panel_inicio.router)
app.include_router(docente_vinculacion.router)