setup:
	cp .env-template .env
	uv venv --python 3.13.3
	uv sync

lint:
	docker compose exec app uv run ruff check .
	docker compose exec app uv run ruff format .
	docker compose exec app uv run mypy src/

idb:
	docker compose exec app sqlite3 data/app.db
