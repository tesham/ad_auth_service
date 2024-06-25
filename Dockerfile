FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disk and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install PostgreSQL client and development packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependdencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 8001

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "auth_service.wsgi:application"]