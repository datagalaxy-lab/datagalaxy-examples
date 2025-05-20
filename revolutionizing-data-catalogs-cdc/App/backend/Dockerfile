# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Prevents Python from writing pyc files to disc & buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
