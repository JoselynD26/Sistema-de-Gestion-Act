import requests, json

BASE_URL = "http://localhost:8000"

# Admin credentials (ensure these exist in DB)
admin_email = "admin@example.com"
admin_password = "admin123"

# Login as admin
login_resp = requests.post(f"{BASE_URL}/usuarios/login/", json={"correo": admin_email, "contrasena": admin_password})
if login_resp.status_code != 200:
    raise Exception(f"Admin login failed: {login_resp.status_code} {login_resp.text}")
access_token = login_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Create a test user (docente) if not exists
new_user = {
    "nombres": "Test",
    "apellidos": "User",
    "correo": "testuser@example.com",
    "contrasena": "testpass",
    "rol": "docente",
    "id_docente": None
}
create_resp = requests.post(f"{BASE_URL}/usuarios/", json=new_user, headers=headers)
if create_resp.status_code not in (200, 201):
    raise Exception(f"User creation failed: {create_resp.status_code} {create_resp.text}")
user_id = create_resp.json()["id"]

# Admin updates the user via new endpoint
update_payload = {"correo": "updated@example.com", "nombres": "UpdatedName"}
update_resp = requests.put(f"{BASE_URL}/usuarios/admin/{user_id}", json=update_payload, headers=headers)
print("Update status:", update_resp.status_code)
print("Response body:", json.dumps(update_resp.json(), indent=2))
