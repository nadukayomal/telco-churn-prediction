.PHONY: all clean install  help

PYTHON = python
VENV_DIR = .tcp
MLFLOW_PORT=5001

ifeq ($(OS),Windows_NT)
    VENV_PY = $(VENV_DIR)/Scripts/python.exe
else
    VENV_PY = $(VENV_DIR)/bin/python
endif

all : help

help :
	@echo "Available targets:"
	@echo "  make install            - Install project dependencies and set up environment"
	@echo "  make install-dev        - Install project with development dependencies"
	@echo "  make data-pipeline      - Run the data processing pipeline"
	@echo "  make training-pipeline  - Run the ML model training pipeline"
	@echo "  make inference-pipeline - Run the model inference pipeline"
	@echo "  make mlflow-ui          - Launch the MLflow tracking UI server"
	@echo "  make clean              - Remove virtual environment and clean up"

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

data-pipeline:
	@echo "Start running data pipeline..."
	@$(VENV_PY) ml_pipeline/data_pipeline.py
	@echo "Data pipeline completed successfully!"

training-pipeline:
	@echo "Start running training pipeline..."
	@$(VENV_PY) ml_pipeline/training_pipeline.py
	@echo "Training pipeline completed successfully!"

inference-pipeline:
	@echo "Start running inference pipeline..."
	@$(VENV_PY) ml_pipeline/inference_pipeline.py
	@echo "Inference pipeline completed successfully!"

mlflow-ui:
	@echo "Launch MLflow UI..."
	@echo "MLflow UI will be available at: http://localhost:$(MLFLOW_PORT)"
	@echo "Press ctrl+c to stop the server"
	@.tcp\Scripts\mlflow ui --host 0.0.0.0 --port $(MLFLOW_PORT)

clean :
	@echo "Cleaning up..."
	@if exist $(VENV_DIR) rmdir /s /q $(VENV_DIR)
	@echo "Virtual environment removed."

