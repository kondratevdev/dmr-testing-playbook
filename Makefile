SHELL := /bin/bash
.DEFAULT_GOAL := help

# Keep command targets deterministic: use `make install` to update the env.
export UV_NO_SYNC := 1

.PHONY: help install format lint type-check test package check run clean

help: ## List available commands
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z][a-zA-Z0-9_-]*:.*##/ {printf "%-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all development dependencies
	uv sync --all-groups

format: ## Format code with Ruff
	uv run python -m ruff format
	uv run python -m ruff check

lint: ## Run Ruff and WPS/Flake8
	uv run python -m ruff check --exit-non-zero-on-fix
	uv run python -m ruff format --check --diff
	uv run python -m flake8 .

type-check: ## Run Mypy
	uv run python -m mypy .

test: ## Run Django system checks and pytest suite
	cd playbook && uv run python manage.py check
	cd playbook && uv run pytest

package: ## Validate the lock file and installed dependencies
	uv lock --check
	uv sync --all-groups --locked --check
	uv pip check

check: lint type-check test package ## Run all project checks

run: ## Start the Django development server
	cd playbook && uv run python manage.py runserver

clean: ## Remove local tool caches
	rm -rf .mypy_cache .ruff_cache
