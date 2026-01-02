import requests
from datetime import date

BASE_URL = "http://localhost:8000"

def test_cancellation():
    try:
        # 1. Fetch a valid HorarioDocente ID
        print("Fetching existing recurring schedules...")
        response = requests.get(f"{BASE_URL}/horario-docente/")
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch schedules: {response.text}")
            return
            
        schedules = response.json()
        if not schedules:
            print("❌ No recurring schedules found in DB. Cannot test cancellation.")
            return
            
        horario_id = schedules[0]['id']
        print(f"Using Horario ID: {horario_id}")
        
        # 2. Register cancellation
        payload = {
            "horario_id": horario_id,
            "fecha": str(date.today()),
            "motivo": "Prueba de cancelación automática",
            "estado": "cancelado"
        }
        
        print(f"Sending POST request to {BASE_URL}/horarios/cancelados/ with payload: {payload}")
        response = requests.post(f"{BASE_URL}/horarios/cancelados/", json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        
        if response.status_code in [200, 201]:
            print("✅ Cancellation registered successfully")
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_cancellation()
