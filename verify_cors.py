import requests

url = "http://localhost:8000/auth/login"
headers = {
    "Origin": "http://localhost:3000",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "Content-Type"
}

try:
    response = requests.options(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        if "access-control" in key.lower():
            print(f"  {key}: {value}")
except Exception as e:
    print(f"Error: {e}")
