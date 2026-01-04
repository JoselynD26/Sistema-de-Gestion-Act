from app.core.config import SessionLocal, engine
from app.models.usuario import Usuario
from sqlalchemy import text

print(f"Engine URL: {engine.url}")

db = SessionLocal()
try:
    # Query using ORM
    query = db.query(Usuario).filter(Usuario.rol == "admin")
    print(f"ORM Query SQL: {query.statement}")
    admins = query.all()
    print(f"ORM Admins found: {len(admins)}")
    
    # Query using raw SQL
    result = db.execute(text("SELECT count(*) FROM usuario WHERE rol = 'admin'")).scalar()
    print(f"Raw SQL count: {result}")
    
    # Check all roles
    roles = db.execute(text("SELECT DISTINCT rol FROM usuario")).fetchall()
    print(f"Distinct roles in DB: {[r[0] for r in roles]}")

finally:
    db.close()
