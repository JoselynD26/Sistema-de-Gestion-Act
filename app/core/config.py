from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from pydantic import EmailStr

# -------------------
# Cargar variables de entorno (solo para local)
# -------------------
load_dotenv()

# -------------------
# URL de conexión (Render o local)
# -------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------
# Configuración SMTP (FastAPI-Mail)
# -------------------
MAIL_USERNAME = os.getenv("SMTP_USERNAME")
MAIL_PASSWORD = os.getenv("SMTP_PASSWORD")
MAIL_FROM = os.getenv("SMTP_FROM_EMAIL")
MAIL_PORT = int(os.getenv("SMTP_PORT", 587))
MAIL_SERVER = os.getenv("SMTP_SERVER")
MAIL_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Sistema Yavirac")
ADMIN_EMAIL = os.getenv("SMTP_FROM_EMAIL") # Por defecto usamos el mismo del remitente o uno específico

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

# -------------------
# Crear motor y sesión
# -------------------
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=30
    )
    print("✅ Motor de base de datos creado exitosamente")
except Exception as e:
    print(f"❌ ERROR al crear motor de base de datos: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------
# Base para modelos
# -------------------
Base = declarative_base()

# -------------------
# Dependencia para obtener sesión de base de datos
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
