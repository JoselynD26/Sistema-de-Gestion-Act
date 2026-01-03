from app.core.config import engine
from sqlalchemy import inspect

try:
    inspector = inspect(engine)
    columns = inspector.get_columns('usuario')
    with open("db_columns.txt", "w") as f:
        f.write("Columnas en tabla 'usuario':\n")
        for column in columns:
            f.write(f"- {column['name']} ({column['type']})\n")

        names = [c['name'] for c in columns]
        if 'nombres' not in names:
            f.write("\n⚠️ AVISO: Columna 'nombres' NO encontrada.\n")
        else:
            f.write("\n✅ Columna 'nombres' encontrada.\n")
    print("Done writing to file.")
        
except Exception as e:
    print(f"Error inspeccionando DB: {e}")
