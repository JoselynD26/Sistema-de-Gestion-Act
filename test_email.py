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
        # Test 1: Admin verification
        print("\n--- Testing Admin Verification Email ---")
        success_admin = await email_service.send_admin_verification_email("test@example.com", "Test User (Antigravity)")
        
        # Test 2: Password recovery
        print("\n--- Testing Password Recovery Email ---")
        # Note: In a real test, this would use a real email from the DB or mock it.
        # But we just want to see if the utility sends the email.
        success_rec = await email_service.send_password_recovery_email("joselyndicao2004@gmail.com", "ABC12345", "Joselyn (Test)")
        
        print(f"\nRESULTS: Admin success={success_admin}, Recovery success={success_rec}")
        
    except Exception as e:
        print(f"EXCEPTION in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
