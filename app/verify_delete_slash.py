import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app
from app.api.reserva_aulas import router

client = TestClient(app)

def test_delete_endpoint():
    print("Testing DELETE /reserva-aulas/99999/ (with trailing slash)...")
    try:
        # We use a non-existent ID just to check routing/status code behavior, not actual deletion logic yet
        # Expecting 404 (Not Found) if it reaches the endpoint, or 307 (Redirect) if strict slashes
        response = client.delete("/reserva-aulas/99999/", follow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 307:
            print("RESULT: Redirect detected (FastAPI default behavior). Frontend might need to follow redirects or we fix backend.")
        elif response.status_code == 404:
             print("RESULT: Endpoint reached (404 is good here, means routing worked).")
        elif response.status_code == 405:
            print("RESULT: Method Not Allowed. Trailing slash might be treating it as directory?")
        else:
             print(f"RESULT: Unexpected status {response.status_code}")

    except Exception as e:
        print(f"ERROR: {e}")

    print("\nTesting DELETE /reserva-aulas/99999 (NO trailing slash)...")
    try:
        response = client.delete("/reserva-aulas/99999", follow_redirects=False)
        print(f"Status Code: {response.status_code}") 
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_delete_endpoint()
