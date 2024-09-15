import sys
from uvicorn import run
import create_database

def start():
    run("fastapi_app.app.main:app", host="127.0.0.1", port=8001, reload=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py [start]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "start":
        start()

    elif command == "migrate":
        create_database.migrate()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()