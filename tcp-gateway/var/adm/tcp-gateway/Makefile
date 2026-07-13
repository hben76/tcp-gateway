.PHONY: run test lint format check clean

run:
	uvicorn app.main:app --reload --port 59876

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

check: format lint test

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
