# Downloading image python
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# Set up working directory
WORKDIR /app

## System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Requirements.txt
COPY requirements.txt .

# Setup requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .


# Create directory for mediafiles
RUN mkdir -p /app/media

# Set up [ort for Django
EXPOSE 8000

# Start command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]