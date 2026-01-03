import asyncio
from app.services.email_service import email_service
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    print("Testing admin verification email (Async version)...")
    print(f"SMTP Server: {os.getenv('SMTP_SERVER')}")
    print(f"SMTP User: {os.getenv('SMTP_USERNAME')}")
    print(f"SMTP From: {os.getenv('SMTP_FROM_EMAIL')}")

    try:
        # Trigger the async service
        # Note: This will fetch real admins from DB and try to send real emails if configured!
        success = await email_service.send_admin_verification_email("test@example.com", "Test User (Antigravity)")
        if success:
            print("SUCCESS: Email task triggered successfully")
        else:
            print("FAILURE: Service returned False")
    except Exception as e:
        print(f"EXCEPTION in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
