STORAGE_PATH = .local_dev/docker-compose.storage.local.yml
DC = docker compose

ALEMBIC = alembic

.PHONY: infra type format lint env migrate upgrade downgrade revision test

infra:
	$(DC) -f $(STORAGE_PATH) up --build -d

type:
	mypy ./src

format:
	ruff format .


lint:
	ruff check ./src --fix

env:
	cp .env.template .env


migrate:
	$(ALEMBIC) upgrade head

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
	$(ALEMBIC) downgrade -1

revision:
	$(ALEMBIC) revision --autogenerate -m "$(m)"


test:
	PYTHONPATH=src pytest tests/units