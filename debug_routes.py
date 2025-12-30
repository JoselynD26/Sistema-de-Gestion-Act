from main import app
import sys

with open("routes.txt", "w", encoding="utf-8") as f:
    f.write("--- Registered Routes ---\n")
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            f.write(f"{route.path} methods={route.methods}\n")
        else:
            name = getattr(route, 'path', 'Unknown')
            f.write(f"Mount: {name}\n")
