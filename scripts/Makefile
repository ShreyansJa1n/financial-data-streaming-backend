.PHONY: install_dependencies run_development run_production

install_dependencies:
	@echo "Installing dependencies..."
	@pip install -r ../requirements/requirements.txt
	@echo "Dependencies installed successfully."

run_development: install_dependencies
	@echo "Setting up development environment..."
	@echo "Running development server..."
	cd .. && fastapi dev main.py --reload --host 0.0.0.0 --port 8000
	@echo "Development server is running."

run_production:
	@echo "Running production server..."
	fastapi run ../main.py --host 0.0.0.0 --port 8000