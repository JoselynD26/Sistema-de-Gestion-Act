import json
from sqlalchemy import text
from app.core.config import SessionLocal

def compare_docentes():
    db = SessionLocal()
    try:
        # User provided list of IDs (extracted from the JSON)
        # Note: I'll manually check the gaps in IDs provided by the user
        # IDs provided: 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
        # 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40,
        # 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 64, 65, 2, 56, 57, 58, 59, 60,
        # 61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
        # 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
        # 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111
        
        user_ids = [
            1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 64, 65, 2, 56, 57, 58, 59, 60,
            61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
            81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
            101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111
        ]
        print(f"Number of list items provided by user: {len(user_ids)}")
        user_ids.sort()
        
        print(f"User claims to have {len(user_ids)} docentes.")
        print(f"Min ID: {min(user_ids)}, Max ID: {max(user_ids)}")
        
        # Get IDs from DB
        db_ids = [r[0] for r in db.execute(text("SELECT id FROM docente")).fetchall()]
        db_ids.sort()
        
        print(f"DB has {len(db_ids)} docentes.")
        
        missing_in_db = set(user_ids) - set(db_ids)
        extra_in_db = set(db_ids) - set(user_ids)
        
        if missing_in_db:
            print(f"Missing in DB (but in User message): {sorted(list(missing_in_db))}")
        else:
            print("No IDs from the user list are missing in the DB.")
            
        if extra_in_db:
            print(f"Extra in DB (not in User message): {sorted(list(extra_in_db))}")

    finally:
        db.close()

if __name__ == "__main__":
    compare_docentes()
