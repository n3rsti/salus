from python:3.14-slim

workdir /app

copy ./api /app

run pip install -r requirements.txt

expose 8080

cmd ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]
