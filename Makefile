setup:
	cp .env-template .env
	uv venv --python 3.13.3
	uv sync

lint:
	uv run ruff check .
	uv run ruff format .
	uv run mypy src/

idb:
	docker compose exec app sqlite3 data/app.db

seed:
	docker compose exec app uv run python scripts/seed_users.py
