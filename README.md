# Code Repository Explorer

Explore and ask questions about a GitHub code repository using Ollama supplied language model.

## Prerequisites

- Python 3.11 - Runtime environment for this repository (https://www.python.org/downloads/release/python-3117/)
- Poetry - Python packaging and dependency management made easy (https://github.com/python-poetry/poetry)
- Ollama - Get up and running with large language models locally (https://github.com/ollama/ollama)

## Usage
1. Set up Ollama with a model, for example: https://ollama.ai/library/mistral
2. Set up the model name in `.env` file cloned from `.env.example`: `OLLAMA_MODEL=mistral`
3. Install the repository dependencies using poetry: `poetry install --sync`
3. Run the script: `poetry run python app.py`
3. Enter the GitHub URL of the repository to explore.
4. Ask questions about the repository. Type `exit()` to quit.

## Key Features
- Clones and indexes the contents of a GitHub repository.
- Supports various file types, including code, text, and Jupyter Notebook files.
- Generates detailed answers to user queries based on the repository's contents.
- Uses Ollama supplied model for generating responses.
- Supports interactive conversation with the language model.
- Presents top relevant documents for each question.
