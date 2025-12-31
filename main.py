from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

# Importación de rutas desde app/api
from app.api import (
    docente, aula, materia, reserva,
    carrera, curso, horario, plaza, sede, sala_profesores, escritorio,
    # materia_carrera, sala_carrera, # Eliminado
    curso_aula, curso_horario,
    # docente_materia, docente_carrera, # Eliminado
    auth, docente_vinculacion,
    usuario, usuario_rol, rol, permiso, rol_permiso,
    notificacion, croquis, curso_vinculacion, panel_inicio,
    sala, reserva_aulas, profesor_panel, pdf_horarios, horario_docente
)

app = FastAPI(
    title="Sistema Académico",
    description="API protegida con JWT por rol",
    version="1.0.0"
)

# -------------------
# Seguridad global para Swagger
# -------------------
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

# -------------------
# CORS para permitir acceso desde frontend Flutter Web
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir a ["http://localhost:49711"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando"}

# -------------------
# Rutas principales
# -------------------
app.include_router(docente.router)
app.include_router(aula.router)
app.include_router(materia.router, prefix="/materias", tags=["Materias"])
app.include_router(reserva.router, prefix="/reservas", tags=["Reservas"])
app.include_router(carrera.router)
app.include_router(curso.router)
app.include_router(horario.router, prefix="/horarios", tags=["Horarios"])
app.include_router(plaza.router)
app.include_router(sede.router)
app.include_router(sala_profesores.router, prefix="/sala-profesores", tags=["Sala Profesores"])
app.include_router(escritorio.router)
# app.include_router(materia_carrera.router) # Eliminado
# app.include_router(sala_carrera.router)    # Eliminado
app.include_router(curso_aula.router)
app.include_router(curso_horario.router)
# app.include_router(docente_materia.router) # Eliminado
# app.include_router(docente_carrera.router) # Eliminado
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
app.include_router(escritorio.router, prefix="/escritorios", tags=["Escritorios"])
app.include_router(horario_docente.router)


# ✅ Router de Salas
# Como en app/api/sala.py ya definiste las rutas sin prefijo (/ , /sede/{id}, /{id}),
# aquí sí usamos prefix="/salas" para que queden limpias:
#   POST /salas/
#   GET /salas/sede/{id}
#   GET /salas/{id}
#   PUT /salas/{id}
#   DELETE /salas/{id}
app.include_router(sala.router, prefix="/salas", tags=["Salas"])
app.include_router(reserva_aulas.router, prefix="/reserva-aulas", tags=["Reserva Aulas"])
app.include_router(profesor_panel.router, prefix="/profesor", tags=["Panel Profesor"])
app.include_router(croquis.router, prefix="/croquis", tags=["Croquis"])
app.include_router(pdf_horarios.router, prefix="/pdf-horarios", tags=["PDF Horarios"])
app.include_router(horario.router, prefix="/horarios", tags=["Horarios"])


# Servir archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")