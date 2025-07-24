# Use an official Python runtime as base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y build-essential libsndfile1 ffmpeg && \
    apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Create upload directory
RUN mkdir -p uploads

# Expose the port Flask runs on
EXPOSE 5000

# Start the app with Gunicorn
CMD ["gunicorn", "app:create_app", "--bind", "0.0.0.0:5000", "--timeout", "90"]
