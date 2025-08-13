# Python configuration
PYTHON=python3
PIP=pip3
VENV=.venv

# Project directories
BACKEND_DIR=backend
FRONTEND_DIR=frontend

# Default target
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make setup      - Set up both backend and frontend"
	@echo "  make install    - Install Python dependencies"
	@echo "  make run       - Run the backend server"
	@echo "  make frontend  - Install and run frontend"
	@echo "  make clean     - Clean up generated files"
	@echo "  make test      - Run tests"

.PHONY: setup
setup: install frontend

.PHONY: install
install:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov

.PHONY: frontend
frontend:
	cd $(FRONTEND_DIR) && npm install

.PHONY: run
run:
	$(PYTHON) app.py

.PHONY: run-frontend
run-frontend:
	cd $(FRONTEND_DIR) && npm start

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf $(FRONTEND_DIR)/node_modules

.PHONY: test
test:
	$(PYTHON) -m pytest tests/
