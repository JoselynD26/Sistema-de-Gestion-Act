"""
Script para probar peticiones OPTIONS (CORS preflight)
"""
import requests

# URL del servidor
url = "http://localhost:8000/login/"

# Headers para simular una petición preflight
headers = {
    "Origin": "https://front-sistema-8hz.pages.dev",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type",
}

print("🧪 Probando petición OPTIONS (CORS preflight)...")
print(f"URL: {url}")
print(f"Headers: {headers}\n")

try:
    response = requests.options(url, headers=headers)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Headers de respuesta:")
    for key, value in response.headers.items():
        if "access-control" in key.lower() or "origin" in key.lower():
            print(f"   {key}: {value}")
    
    if response.status_code == 200:
        print("\n✅ CORS preflight funcionando correctamente!")
    else:
        print(f"\n❌ Error: Se esperaba 200, se recibió {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
