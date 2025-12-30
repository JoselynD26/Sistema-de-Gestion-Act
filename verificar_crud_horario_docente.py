import requests
import json
from datetime import time

BASE_URL = "http://127.0.0.1:8001/horario-docente"

def test_crud_horario_docente():
    print("--- Probando CRUD Horario Docente ---")

    # 0. Prueba de Error de Integridad (Optimización)
    print("\n0. Probando creación con IDs inválidos (debería dar 400)...")
    payload_invalid = {
        "docente_id": 999999,
        "curso_id": 999999,
        "materia_id": 1,
        "aula_id": 1,
        "dia": "Lunes",
        "hora_inicio": "08:00:00",
        "hora_fin": "10:00:00"
    }
    resp_inv = requests.post(f"{BASE_URL}/", json=payload_invalid)
    if resp_inv.status_code == 400:
        print("✅ Correcto: Se recibió 400 Bad Request por integridad referencial (Optimizado).")
    else:
        print(f"⚠️ Advertencia: Se esperaba 400, se recibió {resp_inv.status_code}. Msg: {resp_inv.text}")

    
    # 1. Crear un horario (POST)
    payload = {
        "docente_id": 106,
        "curso_id": 4,
        "materia_id": 1,
        "aula_id": 1,
        "dia": "Lunes",
        "hora_inicio": "08:00:00",
        "hora_fin": "10:00:00"
    }
    
    print("\n1. Creando horario...")
    response = requests.post(f"{BASE_URL}/", json=payload)
    if response.status_code == 200:
        horario = response.json()
        horario_id = horario['id']
        print(f"✅ Horario creado con ID: {horario_id}")
    else:
        print(f"❌ Error al crear horario: {response.status_code}")
        print(response.text)
        return

    # 2. Actualizar el horario (PATCH)
    update_payload = {
        "dia": "Martes",
        "estado": "inactivo"
    }
    print(f"\n2. Actualizando horario ID {horario_id} (PATCH)...")
    # Probando con barra final para verificar compatibilidad
    response = requests.patch(f"{BASE_URL}/{horario_id}/", json=update_payload)
    if response.status_code == 200:
        horario_actualizado = response.json()
        print(f"✅ Horario actualizado: Dia={horario_actualizado['dia']}, Estado={horario_actualizado['estado']}")
    else:
        print(f"❌ Error al actualizar horario: {response.status_code}")
        print(response.text)

    # 3. Eliminar el horario (DELETE)
    print(f"\n3. Eliminando horario ID {horario_id} (DELETE)...")
    response = requests.delete(f"{BASE_URL}/{horario_id}")
    if response.status_code == 200:
        print(f"✅ {response.json()['message']}")
    else:
        print(f"❌ Error al eliminar horario: {response.status_code}")
        print(response.text)

    # 4. Verificar eliminación
    print(f"\n4. Verificando que el horario ya no exista...")
    response = requests.patch(f"{BASE_URL}/{horario_id}/", json=update_payload)
    if response.status_code == 404:
        print("✅ Correcto: El horario ya no existe (404)")
    else:
        print(f"❌ Error: Se esperaba 404 pero se obtuvo {response.status_code}")

if __name__ == "__main__":
    test_crud_horario_docente()
