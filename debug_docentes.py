from sqlalchemy import text
from app.core.config import SessionLocal
from app.schemas.docente import DocenteOut
from pydantic import ValidationError

def debug_docentes():
    db = SessionLocal()
    try:
        # Check all tables named 'docente' in different schemas
        schemas = db.execute(text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'docente'")).fetchall()
        print("\nTables named 'docente' found:")
        for s in schemas:
            count = db.execute(text(f"SELECT count(*) FROM {s[0]}.{s[1]}")).scalar()
            print(f"  - Schema: {s[0]}, Table: {s[1]}, Count: {count}")

        # Get all records from public.docente
        result = db.execute(text("SELECT * FROM public.docente")).fetchall()
        print(f"\nTotal records in 'public.docente' table: {len(result)}")
        
        # Check usuario table
        users = db.execute(text("SELECT count(*) FROM public.usuario")).scalar()
        docente_users = db.execute(text("SELECT count(*) FROM public.usuario WHERE rol = 'docente'")).scalar()
        print(f"Total records in 'public.usuario' table: {users}")
        print(f"Total users with role 'docente': {docente_users}")
        
        passed = 0
        failed = 0
        
        for row in result:
            # Try to map to DocenteOut
            try:
                # Assuming row is a mapping or we can convert to dict
                # SQLAlchemy rows can be converted to dict
                data = dict(row._mapping)
                DocenteOut.model_validate(data)
                passed += 1
            except ValidationError as e:
                failed += 1
                print(f"\nValidation failed for record ID {data.get('id')}:")
                # Print why it failed
                for error in e.errors():
                    print(f"  - {error['loc']}: {error['msg']} (value: {data.get(error['loc'][0])})")
            except Exception as e:
                failed += 1
                print(f"\nUnexpected error for record ID {data.get('id')}: {str(e)}")
        
        print(f"\nSummary:")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Total: {passed + failed}")

    finally:
        db.close()

if __name__ == "__main__":
    debug_docentes()
