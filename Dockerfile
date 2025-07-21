# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Postgres and Pillow (for images, if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the project into the container
COPY . .

# Create a staticfiles directory for collectstatic (used only in prod)
RUN mkdir -p /app/staticfiles

# Expose port 8000 for the app
EXPOSE 8000

# By default, run Gunicorn (for production).
# For development, override this CMD in docker-compose to use runserver.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library_management.wsgi:application"]
