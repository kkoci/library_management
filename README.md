
# Library Management System

A Django REST Framework (DRF)-based **Library Management System** that allows users to browse, search, borrow, and return books. Built as part of the Pixelfield onboarding test task.

---

## Features

- **User Roles:**
  - Anonymous users: Browse/search books (read-only).
  - Registered users: Borrow and return books.
  - Administrators: Manage books and users.

- **Authentication & Authorization:**
  - User registration and login via Django REST Framework.
  - JWT-based authentication (`djangorestframework-simplejwt`).

- **Core Models:**
  - **CustomUser**: Extends Django’s `AbstractUser`.
  - **Book**: Title, author, ISBN, genre, publication date, availability, cover image.
  - **Loan**: Tracks which user borrowed which book and when.

- **Filtering & Pagination:**
  - Implemented via `BookFilter` (Django Filters).
  - Supports searching by title, author, genre, publication year, and filtering by availability.
  - Paginated book lists (20 per page by default).

- **API Documentation:**
  - **Swagger UI**: `/swagger/`
  - **Redoc**: `/redoc/`

- **Testing:**
  - Unit tests for models, serializers, and views.
  - Integration tests for API flows.
  - **Run locally**: `python manage.py test books.tests users.tests loans.tests --verbosity=2`
  - **Run via Docker**: `docker-compose run --rm test`

- **Security:**
  - **Custom `SecurityMiddleware`** blocks suspicious patterns (XSS, SQL Injection attempts) by decoding full URL/query and POST data.
  - Adds strict security headers: `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`.
  - Django ORM used exclusively (prevents SQL injection).

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` – User registration
- `POST /api/auth/login/` – User login
- `POST /api/auth/logout/` – User logout
- `GET /api/auth/profile/` – Get/update user profile
- `POST /api/auth/token/refresh/` – Refresh JWT token

### Books
- `GET /api/books/` – List all books (with filtering, search, pagination)
- `POST /api/books/` – Create new book (Admin only)
- `GET /api/books/{id}/` – Get book details
- `PUT /api/books/{id}/` – Update book (Admin only)
- `DELETE /api/books/{id}/` – Delete book (Admin only)
- `GET /api/books/stats/` – Get book statistics

### Loans
- `GET /api/loans/` – List all loans (user’s own loans or all for admins)
- `POST /api/loans/create/` – Borrow a book (creates a loan)
- `POST /api/loans/{id}/return/` – Return a borrowed book
- `GET /api/loans/my-loans/` – List current user’s loans
- `GET /api/loans/stats/` – Loan statistics (Admin only)

---

## Project Structure

    library_management/
    ├── books/ # Book model, views, serializers, filters, tests, and populate script
    │ ├── filters.py
    │ ├── management/commands/populate_books.py
    │ └── tests/
    ├── loans/ # Loan model, API views, and tests
    │ └── tests/
    ├── users/ # Custom user model, registration/login API, and tests
    │ └── tests/
    ├── library_management/ # Settings, URLs, middleware (SecurityMiddleware)
    │ └── middleware.py
    ├── .github/workflows/ # GitHub Actions CI (runs tests on push)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── .env
    └── manage.py


---

## Local Setup (without Docker)

### Requirements
- Python 3.11+
- Virtualenv
- SQLite (for local dev/testing)

### Steps`bash

    git clone https://github.com/kkoci/library_management.git
    cd library_management

# Create & activate virtualenv

    python -m venv venv
    source venv/bin/activate      # macOS/Linux
    venv\Scripts\activate         # Windows

# Install dependencies

    pip install -r requirements.txt

# Configure environment

    cp .env.example .env

# Run migrations & seed data

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py populate_books

# Start development server

    python manage.py runserver
    App: http://localhost:8000
    Swagger: http://localhost:8000/swagger/
    Redoc: http://localhost:8000/redoc/

Running with Docker

    docker-compose up --build
    Runs web app on port 8000
    Starts PostgreSQL DB container
    Seeds the database with sample books
    Runs all tests in a dedicated container

## Run tests manually:

    docker-compose run --rm test

## Environment Variables

.env example:

    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///db.sqlite3
    ALLOWED_HOSTS=localhost,127.0.0.1

For PostgreSQL in Docker:

    DATABASE_URL=postgresql://library_user:password@db:5432/library

Testing

    Local:
    python manage.py test books.tests users.tests loans.tests --verbosity=2
    Docker:
    docker-compose run --rm test

## License
MIT License – see LICENSE for details.
