# Cinema Project

A Django REST API for managing a cinema: movies, screening schedules, halls, and ticket bookings.

## Features

- **Movies** – CRUD for movies and genres with filtering by genre/language
- **Cinema** – Manage halls, seats, and screenings (filterable by movie/date)
- **Bookings** – Authenticated users can book seats for a screening
- **Accounts** – User registration and profile management

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register/` | Register a new user |
| GET/PUT | `/api/auth/profile/` | View or update your profile |
| GET | `/api/movies/` | List all movies |
| GET | `/api/movies/genres/` | List all genres |
| GET | `/api/cinema/halls/` | List cinema halls |
| GET | `/api/cinema/screenings/` | List screenings (filter: `?movie=<id>&date=YYYY-MM-DD`) |
| GET | `/api/cinema/seats/` | List seats (filter: `?hall=<id>`) |
| GET/POST | `/api/bookings/` | List or create bookings (auth required) |

Visit `/admin/` to manage all data via Django Admin.

## Running Tests

```bash
python manage.py test
```
