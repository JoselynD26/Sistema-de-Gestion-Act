from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import (
    docente, aula, materia, reserva,
    carrera, curso, horario, plaza, sede, sala_profesores, escritorio,
    curso_aula, curso_horario,
    auth, docente_vinculacion,
    usuario, usuario_rol, rol, permiso, rol_permiso,
    notificacion, croquis, curso_vinculacion, panel_inicio,
    sala, reserva_aulas, profesor_panel, pdf_horarios, horario_docente
)

app = FastAPI(
    title="Sistema Académico",
    description="API protegida con JWT por rol",
    version="1.0.0",
    redirect_slashes=False
)

# =========================
# 🔥 CORS GLOBAL (BASE)
# =========================
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://front-sistema-8hz.pages.dev",
    "https://sistema-de-gestion-act-bj8j.onrender.com",
    "https://sistemagestionyavirac.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando"}

# =========================
# RUTAS
# =========================
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(docente.router)
app.include_router(aula.router)
app.include_router(materia.router, prefix="/materias")
app.include_router(reserva.router, prefix="/reservas")
app.include_router(carrera.router)
app.include_router(curso.router)
app.include_router(horario.router, prefix="/horarios")
app.include_router(plaza.router)
app.include_router(sede.router)
app.include_router(sala_profesores.router, prefix="/sala-profesores")
app.include_router(escritorio.router, prefix="/escritorios")
app.include_router(horario_docente.router)
app.include_router(reserva_aulas.router, prefix="/reserva-aulas")
app.include_router(profesor_panel.router, prefix="/profesor")
app.include_router(pdf_horarios.router, prefix="/pdf-horarios")
app.include_router(croquis.router, prefix="/croquis")
app.include_router(sala.router, prefix="/salas")

# =========================
# STATIC FILES
# =========================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
