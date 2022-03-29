## @ Docker Commands
.PHONY: build up down run restart
build: ## Create the image of dockerfile
	docker-compose build

up: ## Start the application
	docker-compose up -d

down: ## Remove the docker images and containers
	docker-compose down

run: ## Build and run the application
	docker-compose up --build -d

restart: down run ## Rebuild all application

## @ Helper Commands
.PHONY: requirements help
requirements: ## Update requirements.txt
	poetry export --without-hashes -f requirements.txt > requirements.txt

help: ## Show this help.
	python help.py
