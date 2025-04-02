FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY config/ config/
COPY loaders/ loaders/
COPY llm/ llm/
COPY prompts/ prompts/
COPY utils/ utils/
COPY main.py .

# Create necessary directories
RUN mkdir -p storage/documents cache

RUN uv sync --frozen

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"]
