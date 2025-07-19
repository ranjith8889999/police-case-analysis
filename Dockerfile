FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for pgvector and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories needed by the app
RUN mkdir -p /app/app/static/uploads
RUN mkdir -p /app/model_cache
RUN mkdir -p /app/vector_db

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
