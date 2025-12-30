from main import app

found = False
count = 0
with open("url_check.txt", "w", encoding="utf-8") as f:
    for route in app.routes:
        if hasattr(route, "path"):
            count += 1
            if "login" in route.path:
                msg = f"FOUND: {route.path} {route.methods}"
                print(msg)
                f.write(msg + "\n")
                found = True

    f.write(f"Total routes with path: {count}\n")
    if not found:
        f.write("LOGIN ROUTE NOT FOUND\n")
