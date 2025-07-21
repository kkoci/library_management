# Library Management System

A comprehensive library management system built with Django REST Framework, featuring user authentication, book management, and loan tracking.

## Features

### User Management
- User registration and authentication with JWT tokens
- Role-based access control (Admin/Regular User)
- User profiles with additional information

### Book Management
- Complete CRUD operations for books
- Advanced filtering and search capabilities
- Pagination support
- Genre categorization
- Availability tracking

### Loan Management
- Book borrowing and returning system
- Automatic due date calculation
- Overdue tracking with fine calculation
- User loan history

### Security Features
- JWT authentication
- CSRF protection
- XSS protection
- SQL injection prevention
- Role-based permissions

### API Documentation
- Swagger UI integration
- Comprehensive API documentation
- Interactive API testing

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Documentation**: drf-yasg (Swagger)
- **Testing**: pytest, coverage
- **Containerization**: Docker
- **Deployment**: Heroku ready

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd library_management
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Populate with sample data (optional):
```bash
python manage.py populate_books
```

8. Run the development server:
```bash
python manage.py runserver
```

### Docker Development

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get/Update user profile
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Books
- `GET /api/books/` - List all books (with filtering and search)
- `POST /api/books/` - Create new book (Admin only)
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/` - Update book (Admin only)
- `DELETE /api/books/{id}/` - Delete book (Admin only)
- `GET /api/books/stats/` - Get book statistics

### Loans
- `GET /api/loans/` - List loans (user's loans or all for admin)
- `POST /api/loans/create/` - Create new loan
- `POST /api/loans/{id}/return/` - Return a book
- `GET /api/loans/my-loans/` - Get current user's loans
- `GET /api/loans/stats/` - Get loan statistics (Admin only)

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=.
```

Generate coverage report:
```bash
coverage html
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

5. Deploy:
```bash
git push heroku main
```

6. Run migrations:
```bash
heroku run python manage.py migrate
```

7. Create superuser:
```bash
heroku run python manage.py createsuperuser
```

### Docker Production

1. Build production image:
```bash
docker build -t library-management .
```

2. Run with production database:
```bash
docker run -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
           -e SECRET_KEY="your-secret-key" \
           -e DEBUG=False \
           -p 8000:8000 \
           library-management
```

## API Documentation

Access the API documentation at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Admin Panel

Access the Django admin panel at:
- `http://localhost:8000/admin/`

## Project Structure

```
library_management/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .env.example
├── library_management/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests/
├── books/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── filters.py
│   └── tests/
└── loans/
    ├── models.py
    ├── views.py
    ├── serializers.py
    └── tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.
