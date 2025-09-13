.PHONY: help install dev sync test lint format typecheck clean run shell docs pre-commit setup

help:
	@echo "Available commands:"
	@echo "  make install    - Install project dependencies"
	@echo "  make dev        - Install development dependencies"
	@echo "  make sync       - Sync all dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make typecheck  - Run type checking"
	@echo "  make clean      - Clean cache and build files"
	@echo "  make run        - Run the main application"
	@echo "  make shell      - Start Python shell"
	@echo "  make docs       - Build documentation"
	@echo "  make pre-commit - Run pre-commit hooks"
	@echo "  make setup      - Initial project setup"

install:
	uv sync --no-dev

dev:
	uv sync

sync:
	uv sync --all-extras

test:
	uv run pytest -v

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run pyright

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true

run:
	uv run python -m terminal_ai_agents_workshop

shell:
	uv run python

docs:
	uv run sphinx-build -b html docs docs/_build

pre-commit:
	uv run pre-commit run --all-files

setup: dev
	uv run pre-commit install
	@echo "Project setup complete!"