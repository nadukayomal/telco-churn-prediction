.PHONY: all clean install  help

PYTHON = python
VENV_DIR = .tcp

ifeq ($(OS),Windows_NT)
    VENV_PY = $(VENV_DIR)/Scripts/python.exe
else
    VENV_PY = $(VENV_DIR)/bin/python
endif

all : help

help :
	@echo "Available targets:"
	@echo "  make install             - Install project dependencies and set up environment"
	@echo "  make install-dev         - Install project with development dependencies"
	@echo "  make clean               - Remove virtual environment and cache files"

install :
	@echo "Installing project dependencies and setting up environment..."
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Upgrading pip, setuptools and wheel..."
	@$(VENV_PY) -m pip install --upgrade pip setuptools wheel
	@echo "Installing dependencies from pyproject.toml..."
	@$(VENV_PY) -m pip install -e .
	@echo "Installation completed successfully!"
ifeq ($(OS),Windows_NT)
	@echo "To activate the virtual environment, run: .tcp\Scripts\activate"
else
	@echo "To activate the virtual environment, run: source .tcp/bin/activate"
endif

install-dev :
	@echo "Installing project with development dependencies..."
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Upgrading pip, setuptools and wheel..."
	@$(VENV_PY) -m pip install --upgrade pip setuptools wheel
	@echo "Installing dependencies from pyproject.toml with dev extras..."
	@$(VENV_PY) -m pip install -e ".[dev]"
	@echo "Installation completed successfully!"
ifeq ($(OS),Windows_NT)
	@echo "To activate the virtual environment, run: .tcp\Scripts\activate"
else
	@echo "To activate the virtual environment, run: source .tcp/bin/activate"
endif

clean :
	@echo "Cleaning up..."
	@if exist $(VENV_DIR) rmdir /s /q $(VENV_DIR)
	@echo "Virtual environment removed."