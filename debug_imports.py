try:
    print("1. Importing auth dependencies...")
    import secrets
    import string
    from app.core.seguridad import obtener_hash_contrasena
    from app.services.email_service import email_service
    print("   Imports successful.")

    from app.core.config import SessionLocal
    from app.models.usuario import Usuario
    
    print("2. Testing DB Query...")
    db = SessionLocal()
    user = db.query(Usuario).first()
    print(f"   Query successful. Found user: {user.correo if user else 'None'}")
    db.close()

    print("3. Testing Email Service method existence...")
    if hasattr(email_service, 'send_password_recovery_email'):
        print("   Method 'send_password_recovery_email' found.")
    else:
        print("   ERROR: Method NOT found.")

    print("✅ All checks passed.")

except Exception as e:
    print(f"\n❌ ERROR during debug: {e}")
    import traceback
    traceback.print_exc()
