# # Use a slim Python base image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies for Postgres and Pillow (for images, if needed)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt gunicorn

# # Copy the project into the container
# COPY . .

# # Create a staticfiles directory for collectstatic (used only in prod)
# RUN mkdir -p /app/staticfiles

# # Expose port 8000 for the app
# EXPOSE 5000

# # By default, run Gunicorn (for production).
# # For development, override this CMD in docker-compose to use runserver.
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "library_management.wsgi:application"]
# Use a slim Python base image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt gunicorn

# # Copy the project into the container
# COPY . .

# # Collect static files
# RUN python manage.py collectstatic --noinput || true

# # Create necessary directories
# RUN mkdir -p /app/staticfiles

# # Expose port 5000
# EXPOSE 5000

# # Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
#   CMD curl -f http://localhost:5000/health || exit 1

# # Run migrations and start server
# CMD python manage.py migrate --noinput && \
#     gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 60 library_management.wsgi:application
# Use a slim Python base image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p /app/staticfiles

# Expose port 80 instead of 8000
EXPOSE 80

# Run Gunicorn bound to port 80 (so EB’s ALB/NGINX sees it)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library_management.wsgi:application"]
