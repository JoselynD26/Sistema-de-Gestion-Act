import asyncio
from app.utils.email import send_admin_notification, send_status_update_email, send_cancellation_notification
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    print("Testing reservation notifications...")
    test_email = os.getenv("SMTP_FROM_EMAIL") # Sending to self for testing
    
    print(f"Target email for test: {test_email}")
    
    try:
        # Test 1: Admin notification
        print("\n--- Testing Admin Notification (New Reservation) ---")
        await send_admin_notification(
            admin_emails=[test_email, "jose.mandrango@yavirac.edu.ec"],
            reserva_id=999,
            docente_nombre="Test Docente",
            aula_nombre="Aula Magna",
            fecha="2026-01-05",
            hora="08:00 - 10:00"
        )
        
        # Test 2: Status update (Docente)
        print("\n--- Testing Status Update Notification ---")
        await send_status_update_email(
            email_docente=test_email,
            docente_nombre="Test Docente",
            aula_nombre="Aula Magna",
            fecha="2026-01-05",
            nuevo_estado="APROBADA"
        )
        
        # Test 3: Cancellation notification
        print("\n--- Testing Cancellation Notification ---")
        await send_cancellation_notification(
            admin_emails=[test_email],
            reserva_id=999,
            docente_nombre="Test Docente",
            aula_nombre="Aula Magna",
            fecha="2026-01-05"
        )
        
        print("\nTests completed! Check your inbox.")
        
    except Exception as e:
        print(f"EXCEPTION in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
