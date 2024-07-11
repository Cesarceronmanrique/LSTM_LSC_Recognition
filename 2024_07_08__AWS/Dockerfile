# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HNSWLIB_NO_NATIVE=1
ENV AWS_ACCESS_KEY_ID=accesskey
ENV AWS_SECRET_ACCESS_KEY=secretkey

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Gunicorn will listen on this port
EXPOSE 5004

# Start gunicorn with Uvicorn workers. Adjust the number of workers and threads as necessary.
CMD gunicorn -k uvicorn.workers.UvicornWorker -w 12 --threads 3 -b 0.0.0.0:${PORT:-8000} --timeout 120 main:app
