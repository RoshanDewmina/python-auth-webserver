FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev libffi-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install setuptools and wheel
RUN pip install setuptools wheel

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Set working directory
WORKDIR /src

# Install dependencies
COPY requirements.txt .
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser
