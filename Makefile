setup:
	cp .env-template .env
	uv venv --python 3.13.3
	uv sync

dev:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check .
	ruff format .
	mypy src/