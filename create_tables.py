from app.core.config import engine, Base
from app.models.horario_cancelado import HorarioCancelado
# Import other models to ensure they are registered if needed, though usually importing Base is enough if they inherited from it 
# and were imported before. But here we just need HorarioCancelado to be registered.
# It is imported above.

def create_tables():
    print("Creating missing tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    create_tables()