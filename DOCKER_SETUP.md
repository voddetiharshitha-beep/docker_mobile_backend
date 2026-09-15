# Docker Setup Guide

## 1. Project Overview

This project runs the Django backend using Docker containers.

The application architecture is:

   text
Mobile App
    |
    v
Nginx
    |
    v
Gunicorn
    |
    v
Django
    |
    +------------------+
    |                  |
    v                  v
PostgreSQL           Redis
                       |
                       v
                    Celery
....

### Docker Services

The project contains five Docker services:

| Service    | Purpose                    | Port     |
| ---------- | -------------------------- | -------- |
| `web`      | Django + Gunicorn          | `8000`   |
| `postgres` | PostgreSQL database        | `5432`   |
| `redis`    | Redis cache/message broker | `6379`   |
| `celery`   | Celery background worker   | Internal |
| `nginx`    | Reverse proxy              | `80`     |

---

# 2. Installation

## Prerequisites

Install the following:

* Docker Desktop
* Git
* Python 3.13 or compatible Python version
* Visual Studio Code (recommended)

Docker Desktop must be running before starting the project.

## Clone the Project

If the project is stored in Git:

```powershell
git clone <repository-url>
```

Move into the project directory:

```powershell
cd docker_mobile_backend
```

If the Django project is inside the inner directory:

```powershell
cd docker_mobile_backend
```

Verify that the following files exist:

```text
Dockerfile
docker-compose.yml
requirements.txt
manage.py
```

---

# 3. Environment Variables

The Docker Compose configuration provides the following environment variables to Django.

## Django

```text
DJANGO_DEBUG=False
```

This disables Django debug mode for the Docker environment.

## PostgreSQL

```text
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

Django uses the PostgreSQL service name `postgres` as the database hostname because all Docker services are connected to the same Docker network.

## Redis

```text
REDIS_HOST=redis
REDIS_PORT=6379
```

Redis is used by Django caching and Celery.

## Celery

Celery uses Redis as the broker and result backend:

```text
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

---

# 4. Build Commands

## Build all Docker images

From the directory containing `docker-compose.yml`:

```powershell
docker compose build
```

## Build and start everything

```powershell
docker compose up -d --build
```

The `-d` option runs the containers in the background.

## Build only the Django web service

```powershell
docker compose build web
```

## Build only Celery

```powershell
docker compose build celery
```

---

# 5. Start Commands

## Start all services

```powershell
docker compose up -d
```

## Start and rebuild

Use this when Dockerfile or dependency changes have been made:

```powershell
docker compose up -d --build
```

## Check running containers

```powershell
docker compose ps
```

Expected services:

```text
django-web
django-postgres
django-redis
django-celery
django-nginx
```

## Test the Django health API

The application provides:

```text
/api/health/
```

Test through Nginx:

```powershell
curl http://localhost/api/health/
```

Expected response:

```text
{"status": "success", "message": "Django backend is running"}
```

Expected HTTP status:

```text
200 OK
```

---

# 6. Stop Commands

## Stop all services

```powershell
docker compose stop
```

This stops the containers but does not remove them.

## Start stopped services again

```powershell
docker compose start
```

## Stop and remove containers

```powershell
docker compose down
```

## Important: PostgreSQL Data

The PostgreSQL database uses a Docker volume:

```text
postgres_data
```

Therefore, use:

```powershell
docker compose down
```

when you want to stop and remove containers while keeping the database volume.

### Avoid this unless you intentionally want to delete database data:

```powershell
docker compose down -v
```

The `-v` option removes Docker volumes, including the PostgreSQL data volume.

---

# 7. Logs

## View logs for all services

```powershell
docker compose logs
```

## Follow logs in real time

```powershell
docker compose logs -f
```

Press:

```text
Ctrl + C
```

to stop following logs.

## Django web logs

```powershell
docker compose logs web
```

## Show the last 50 Django logs

```powershell
docker compose logs web --tail=50
```

## PostgreSQL logs

```powershell
docker compose logs postgres
```

## Redis logs

```powershell
docker compose logs redis
```

## Celery logs

```powershell
docker compose logs celery
```

## Nginx logs

```powershell
docker compose logs nginx
```

---

# 8. Django Management Commands

Django commands can be executed inside the running web container.

## Run migrations

```powershell
docker compose exec web python manage.py migrate
```

## Create a superuser

```powershell
docker compose exec web python manage.py createsuperuser
```

## Open Django shell

```powershell
docker compose exec web python manage.py shell
```

## Run Django system checks

```powershell
docker compose exec web python manage.py check
```

## Check DEBUG setting

```powershell
docker compose exec web python manage.py shell
```

Then:

```python
from django.conf import settings
print(settings.DEBUG)
```

Expected:

```text
False
```

---

# 9. PostgreSQL

The PostgreSQL service is available inside the Docker network using:

```text
Host: postgres
Port: 5432
Database: django_db
User: django_user
```

Django connects using the Docker service name:

```text
postgres
```

The PostgreSQL data is stored in the Docker volume:

```text
postgres_data
```

---

# 10. Redis

Redis is available to other Docker services using:

```text
Host: redis
Port: 6379
```

Django cache configuration uses Redis.

A basic cache test can be performed with:

```powershell
docker compose exec web python manage.py shell
```

Then:

```python
from django.core.cache import cache

cache.set("docker_test", "Redis is working", timeout=60)

print(cache.get("docker_test"))
```

Expected:

```text
Redis is working
```

---

# 11. Celery

Celery runs as a separate Docker container.

Check Celery:

```powershell
docker compose ps celery
```

View Celery logs:

```powershell
docker compose logs celery --tail=50
```

Celery uses:

```text
Redis DB 0
```

as the broker and:

```text
Redis DB 1
```

as the result backend.

The Celery worker command is:

```powershell
celery -A docker_mobile_backend.celery:app worker --loglevel=info
```

---

# 12. Nginx

Nginx acts as the reverse proxy.

The request flow is:

```text
http://localhost
       |
       v
Nginx :80
       |
       v
Django/Gunicorn :8000
```

Nginx configuration is stored in:

```text
nginx/nginx.conf
```

The Django web service is accessed by Nginx using the Docker service name:

```text
web:8000
```

Test the health endpoint:

```powershell
curl http://localhost/api/health/
```

Expected:

```text
200 OK
```

---

# 13. Troubleshooting

## Problem: Container is not running

Check:

```powershell
docker compose ps
```

Then check logs:

```powershell
docker compose logs <service-name>
```

Example:

```powershell
docker compose logs web --tail=50
```

---

## Problem: Django returns 500 Internal Server Error

Check Django logs:

```powershell
docker compose logs web --tail=50
```

Look for:

```text
Traceback
ModuleNotFoundError
Database connection errors
```

Fix the reported error and restart:

```powershell
docker compose restart web
```

---

## Problem: Nginx returns 502 Bad Gateway

Check that Django is running:

```powershell
docker compose ps web
```

Check Django logs:

```powershell
docker compose logs web --tail=50
```

Check Nginx logs:

```powershell
docker compose logs nginx --tail=50
```

Restart both:

```powershell
docker compose restart web nginx
```

---

## Problem: Nginx is not running

Start Nginx:

```powershell
docker compose up -d nginx
```

Check:

```powershell
docker compose ps nginx
```

---

## Problem: PostgreSQL connection error

Check PostgreSQL:

```powershell
docker compose ps postgres
```

Check logs:

```powershell
docker compose logs postgres --tail=50
```

Verify the Django database settings:

```text
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

Then run:

```powershell
docker compose exec web python manage.py migrate
```

---

## Problem: Redis connection error

Check Redis:

```powershell
docker compose ps redis
```

Check Redis logs:

```powershell
docker compose logs redis --tail=50
```

Test Redis from Django:

```powershell
docker compose exec web python manage.py shell
```

Then:

```python
from django.core.cache import cache

cache.set("test", "Redis OK", timeout=60)

print(cache.get("test"))
```

Expected:

```text
Redis OK
```

---

## Problem: Celery is not connecting to Redis

Check:

```powershell
docker compose logs celery --tail=50
```

The broker should show:

```text
redis://redis:6379/0
```

The result backend should show:

```text
redis://redis:6379/1
```

Restart Celery:

```powershell
docker compose restart celery
```

---

## Problem: DEBUG is still True

Check the Docker environment:

```powershell
docker compose exec web python manage.py shell
```

Then:

```python
from django.conf import settings
print(settings.DEBUG)
```

Expected:

```text
False
```

The Django setting should read:

```python
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
```

---

# 14. Useful Daily Commands

### Start project

```powershell
docker compose up -d
```

### Check services

```powershell
docker compose ps
```

### Test API

```powershell
curl http://localhost/api/health/
```

### View logs

```powershell
docker compose logs -f
```

### Restart everything

```powershell
docker compose restart
```

### Stop project

```powershell
docker compose stop
```

### Remove containers

```powershell
docker compose down
```

### Rebuild after code/configuration changes

```powershell
docker compose up -d --build
```

---

# 15. Verification Checklist

The Docker environment has been verified with:

* [x] Docker Compose configuration
* [x] Django container
* [x] Gunicorn
* [x] PostgreSQL
* [x] PostgreSQL migrations
* [x] Redis
* [x] Django → Redis connection
* [x] Celery
* [x] Celery → Redis connection
* [x] Nginx
* [x] Nginx → Django connection
* [x] Health API
* [x] `DEBUG=False`

Health API verification:

```text
GET /api/health/
HTTP 200 OK
```

Response:

```json
{
    "status": "success",
    "message": "Django backend is running"
}
```

The Dockerized Django backend is successfully running with PostgreSQL, Redis, Celery, Gunicorn, and Nginx.
