build-backend:
	docker build -f api/Dockerfile -t 'salus-api' .

build-frontend:
	docker build -t 'salus-frontend' .

build: build-backend build-frontend

run-backend:
	docker compose -f docker-compose.yaml up salus-api postgres -d

run-frontend:
	docker compose -f docker-compose.yaml up salus-frontend -d

run: run-backend run-frontend
