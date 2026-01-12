build-backend:
	docker build -f api/Dockerfile -t 'salus-api' .

build-frontend:
	docker build -t 'salus-frontend' .

build: build-backend build-frontend

run:
	docker compose -f docker-compose.yaml up -d
