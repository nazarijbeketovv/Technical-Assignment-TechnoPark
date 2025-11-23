STORAGE_PATH = .local_dev/docker-compose.storage.local.yml
DC = docker compose

.PHONY: infra type format lint env

infra:
	$(DC) -f $(STORAGE_PATH) up --build -d

type:
	mypy .

format:
	ruff format .


lint:
	ruff check . --fix

env:
	cp .env.template .env