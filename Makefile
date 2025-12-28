dev:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check .
	ruff format .
	mypy src/