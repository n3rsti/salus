from python:3.14-slim

workdir /app

copy ./ /app

run pip install -r api/requirements.txt

expose 8080

cmd ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8080"]
