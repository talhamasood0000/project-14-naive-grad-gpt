# Naive Grad GPT - Interactive Story Game

.PHONY: setup install-deps run-local run-colab clean help

# Setup virtual environment and install dependencies
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

# Install dependencies for local development
install-deps:
	pip install streamlit
	pip install requests
	pip install pillow
	pip install openai

# Run the Streamlit application locally
run-local:
	cd streamlit-app && streamlit run streamlit-dummy.py

# Setup Jupyter notebook environment for Google Colab
run-colab:
	@echo "Upload Inference.ipynb to Google Colab"
	@echo "Connect to GPU and run all cells"
	@echo "Copy the generated URL and update streamlit-app/pages/start_game.py:9"
	@echo "Add your OpenAI API key to streamlit-app/pages/start_game.py:10"
	@echo "Then run: make run-local"

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf venv/

# Show help
help:
	@echo "Available commands:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  install-deps - Install required Python packages"
	@echo "  run-local   - Run the Streamlit application locally"
	@echo "  run-colab   - Show instructions for Google Colab setup"
	@echo "  clean       - Remove generated files and virtual environment"
	@echo "  help        - Show this help message"