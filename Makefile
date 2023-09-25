include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help up start stop restart status ps clean

up: ## Up all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up $(c)

up-d: ## Up all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up -d $(c)