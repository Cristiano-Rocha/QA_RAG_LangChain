# QA RAG LangChain

A Question-Answering system built with LangChain that uses RAG (Retrieval Augmented Generation) to provide accurate answers based on PDF documents.

## Overview

This project implements a RAG-based question-answering system that:
- Loads and processes PDF documents
- Creates embeddings using Google's text-embedding-004 model
- Stores document chunks in a FAISS vector store
- Uses Gemini for generating responses
- Implements pre and post-processing steps for better results

## Prerequisites

- Python 3.12 or higher
- Google API Key for Gemini and embeddings
- PDF documents to process
- Docker (optional, for containerized deployment)
- VS Code with Remote - Containers extension (optional, for development container)

## Installation

### Local Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t qa-rag-langchain .
```

2. Run the container:
```bash
docker run -v $(pwd)/storage:/app/storage qa-rag-langchain
```

### Development Container Setup

1. Install VS Code and the "Remote - Containers" extension
2. Open the project in VS Code
3. When prompted, click "Reopen in Container"
4. VS Code will build and start the development container

The development container includes:
- Python 3.12
- Pre-configured VS Code extensions
- Automatic code formatting and linting
- Integrated development tools

## Project Structure

```
.
├── .devcontainer/
│   └── devcontainer.json
├── config/
│   ├── __init__.py
│   └── logger.py
├── loaders/
│   ├── __init__.py
│   └── pdf_loader.py
├── llm/
│   └── gemini.py
├── prompts/
│   └── prompts_templates.py
├── utils/
│   └── __init__.py
├── Dockerfile
├── main.py
└── pyproject.toml
```

## Configuration

- Place your PDF documents in the `storage/documents/` directory
- The system will process all PDF files in this directory
- Logs are stored in `qa_rag_langchain.log` and errors in `errors.log`

## Usage

1. Place your PDF documents in the `storage/documents/` directory
2. Run the application:

### Local
```bash
# Run the Streamlit app
streamlit run app.py

# Or run the command line version
python main.py
```

### Docker
```bash
docker run -v $(pwd)/storage:/app/storage qa-rag-langchain
```

The system will:
1. Load and process PDF documents
2. Create embeddings and store them in FAISS
3. Process questions and generate responses using RAG

## Features

- PDF Document Processing
- Semantic Chunking
- Cached Embeddings
- FAISS Vector Store
- Pre and Post-processing steps
- Multi-language support
- Logging system
- Containerized deployment
- Development container with pre-configured tools
- Interactive Streamlit web interface
- Document upload functionality
- Real-time document processing

## Development

For development, additional dependencies are available:
- ruff>=0.11.2 (for linting)
- pytest>=7.0.0 (for testing)

### Testing

The project includes a comprehensive test suite. To run the tests:

```bash
pytest tests/
```

The test suite includes:

1. **Document Processing Tests** (`tests/test_document_processing.py`):
   - Text case conversion
   - Text replacement
   - Document formatting

2. **PDF Loader Tests** (`tests/test_pdf_loader.py`):
   - Loader configuration
   - Document loading
   - File system checks

3. **RAG Chain Tests** (`tests/test_rag_chain.py`):
   - Pre-processing steps
   - Post-processing steps
   - Input validation
   - Output format validation

4. **Common Fixtures** (`tests/conftest.py`):
   - Sample documents
   - Test paths
   - Environment variables

### Development Container Features

The development container includes:
- Python 3.12 environment
- VS Code extensions:
  - Python extension
  - Pylance for better Python language support
  - Ruff for linting
  - Code Spell Checker
- Automatic code formatting on save
- Integrated linting with Ruff
- Consistent development environment across team members

## Dependencies

- beautifulsoup4>=4.13.3
- faiss-cpu>=1.10.0
- langchain>=0.3.21
- langchain-community>=0.3.20
- langchain-experimental>=0.3.4
- langchain-google-genai>=2.1.1
- loguru>=0.7.3
- python-dotenv>=1.0.1
- unstructured[pdf]>=0.17.2

## License

This project is licensed under the MIT License.
