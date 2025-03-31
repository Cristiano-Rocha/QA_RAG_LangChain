FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY config/ config/
COPY loaders/ loaders/
COPY llm/ llm/
COPY prompts/ prompts/
COPY utils/ utils/
COPY main.py .

# Create necessary directories
RUN mkdir -p storage/documents cache

# Install Python dependencies
RUN pip install --no-cache-dir -r <(pipenv requirements)

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"] 