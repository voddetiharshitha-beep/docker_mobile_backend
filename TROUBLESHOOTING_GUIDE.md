# Dockerized Django Backend — Troubleshooting Guide

## 1. Purpose

This guide provides a troubleshooting process for the Dockerized Django backend.

The main troubleshooting flow is:

**Problem**
↓
**Where to check**
↓
**What command/log to inspect**
↓
**Possible solution**

---

# 2. Django / Gunicorn

## Problem: Django backend is not responding

### Where to check

Check the Django/Gunicorn container:

```powershell
docker compose ps web
```

### Inspect logs

```powershell
docker compose logs --tail=100 web
```

To search for common errors:

```powershell
docker compose logs --tail=100 web | Select-String -Pattern "gunicorn|Booting worker|Listening|ERROR|Exception"
```

### Healthy output

Typical healthy messages include:

```text
Starting gunicorn
Listening at: http://0.0.0.0:8000
Booting worker
```

### Possible solutions

Restart the web service:

```powershell
docker compose restart web
```

If code or dependencies changed:

```powershell
docker compose up -d --build web
```

Check Django configuration:

```powershell
docker compose exec web python manage.py check
```

Test the health endpoint:

```powershell
curl.exe -k -i https://localhost/api/health/
```

---

# 3. Nginx

## Problem: Nginx is not serving the application

### Where to check

Check the Nginx container:

```powershell
docker compose ps nginx
```

### Inspect logs

```powershell
docker compose logs --tail=100 nginx
```

Search for common Nginx errors:

```powershell
docker compose logs --tail=100 nginx | Select-String -Pattern "error|warn|failed|connect"
```

### Check Nginx configuration

```powershell
docker exec django-nginx nginx -t
```

Healthy configuration should report:

```text
syntax is ok
test is successful
```

### Possible solutions

Restart Nginx:

```powershell
docker compose restart nginx
```

If the configuration was changed:

```powershell
docker compose up -d --build nginx
```

Test the backend through Nginx:

```powershell
curl.exe -k -i https://localhost/api/health/
```

### Historical issue

A previous Nginx startup error occurred because Markdown code-fence characters were accidentally present in the Nginx configuration:

````text
unknown directive "```"
````

The configuration was corrected and Nginx is currently working.

---

# 4. Celery

## Problem: Celery worker is not processing tasks

### Where to check

Check both Redis and Celery:

```powershell
docker compose ps redis celery
```

### Inspect Celery logs

```powershell
docker compose logs --tail=100 celery
```

Search for important messages:

```powershell
docker compose logs --tail=100 celery | Select-String -Pattern "ERROR|Exception|failed|succeeded|received|ready|Connected"
```

### Healthy output

Look for messages such as:

```text
Connected to redis://redis:6379/0
celery@... ready.
Task ... received
Task ... succeeded
```

### Possible solutions

Restart Redis and Celery:

```powershell
docker compose restart redis celery
```

If the Celery code or dependencies changed:

```powershell
docker compose up -d --build celery
```

### Database task test

The project contains a Celery task that checks PostgreSQL connectivity.

The task should return:

```text
Celery connected to PostgreSQL successfully: 1
```

A successful task confirms that Celery can communicate with PostgreSQL.

---

# 5. PostgreSQL

## Problem: Database connection failure

### Where to check

Check PostgreSQL:

```powershell
docker compose ps postgres
```

### Inspect logs

```powershell
docker compose logs --tail=100 postgres
```

Search for serious database errors:

```powershell
docker compose logs --tail=100 postgres | Select-String -Pattern "ERROR|FATAL|PANIC"
```

### Check Django migrations

```powershell
docker compose exec web python manage.py showmigrations
```

Run migrations when required:

```powershell
docker compose exec web python manage.py migrate
```

### Possible solutions

Restart PostgreSQL:

```powershell
docker compose restart postgres
```

Then check the database health endpoint:

```powershell
curl.exe -k -i https://localhost/api/health/database/
```

A healthy response is:

```json
{
    "status": "healthy",
    "service": "database"
}
```

### Historical PostgreSQL issues

Previous logs contained errors such as:

```text
constraint already exists
password authentication failed
role "postgres" does not exist
```

These were historical events. The database subsequently recovered and reached:

```text
database system is ready to accept connections
```

The current database health endpoint confirms that Django can connect successfully.

Do not reset or delete the database solely because historical errors appear in old logs.

---

# 6. Redis

## Problem: Redis is not available

### Where to check

```powershell
docker compose ps redis
```

### Inspect Redis logs

```powershell
docker compose logs --tail=100 redis
```

Search for errors or startup messages:

```powershell
docker compose logs --tail=100 redis | Select-String -Pattern "ERROR|WARNING|failed|ready|Ready|Ready to accept"
```

### Healthy output

A healthy Redis server reports:

```text
Ready to accept connections tcp
```

### Test Redis directly

```powershell
docker compose exec redis redis-cli ping
```

Expected result:

```text
PONG
```

### Possible solutions

Restart Redis:

```powershell
docker compose restart redis
```

Restart Celery after Redis is available:

```powershell
docker compose restart celery
```

Test the Redis health endpoint:

```powershell
curl.exe -k -i https://localhost/api/health/redis/
```

A healthy response is:

```json
{
    "status": "healthy",
    "service": "redis"
}
```

### Redis security warning

Redis may display a warning that authentication is not enabled.

This is a warning rather than a service failure. In the Docker Compose setup, Redis is used as an internal service.

For a production environment, Redis should be protected using appropriate network restrictions and authentication according to the deployment architecture.

---

# 7. Complete Docker Compose Failure

## Problem: Multiple services are not working

### Check all services

```powershell
docker compose ps
```

Expected services include:

```text
redis
postgres
celery
web
nginx
```

### Inspect all service logs

```powershell
docker compose logs --tail=100
```

### Restart the complete stack

```powershell
docker compose up -d
```

If Docker images or dependencies changed:

```powershell
docker compose up -d --build
```

Then check:

```powershell
docker compose ps
```

---

# 8. Production Health Checks

The application provides three health endpoints.

## Django

```text
/api/health/
```

Expected response:

```json
{
    "status": "success",
    "message": "Django backend is running"
}
```

## PostgreSQL

```text
/api/health/database/
```

Expected response:

```json
{
    "status": "healthy",
    "service": "database"
}
```

## Redis

```text
/api/health/redis/
```

Expected response:

```json
{
    "status": "healthy",
    "service": "redis"
}
```

These endpoints intentionally do not expose database passwords, Redis credentials, secret keys, or connection details.

---

# 9. Recommended Troubleshooting Flow

When the backend has a problem, follow this order:

## Step 1 — Check containers

```powershell
docker compose ps
```

## Step 2 — Check Django/Gunicorn

```powershell
docker compose logs --tail=100 web
```

## Step 3 — Check Nginx

```powershell
docker compose logs --tail=100 nginx
```

## Step 4 — Check Celery

```powershell
docker compose logs --tail=100 celery
```

## Step 5 — Check PostgreSQL

```powershell
docker compose logs --tail=100 postgres
```

## Step 6 — Check Redis

```powershell
docker compose logs --tail=100 redis
```

## Step 7 — Test health endpoints

```powershell
curl.exe -k -i https://localhost/api/health/
curl.exe -k -i https://localhost/api/health/database/
curl.exe -k -i https://localhost/api/health/redis/
```

---

# 10. Quick Service-to-Log Reference

| Service         | Check status                 | View logs                                 |
| --------------- | ---------------------------- | ----------------------------------------- |
| Django/Gunicorn | `docker compose ps web`      | `docker compose logs --tail=100 web`      |
| Nginx           | `docker compose ps nginx`    | `docker compose logs --tail=100 nginx`    |
| Celery          | `docker compose ps celery`   | `docker compose logs --tail=100 celery`   |
| PostgreSQL      | `docker compose ps postgres` | `docker compose logs --tail=100 postgres` |
| Redis           | `docker compose ps redis`    | `docker compose logs --tail=100 redis`    |

---

# 11. Security Rules

Never expose or commit sensitive configuration values.

Do not publish:

```text
SECRET_KEY
DJANGO_SECRET_KEY
POSTGRES_PASSWORD
DATABASE_URL
REDIS_URL
CELERY_BROKER_URL
```

Do not paste secret values into GitHub issues, public documentation, screenshots, or logs.

The troubleshooting guide should contain commands and explanations, not actual credentials.

---

# 12. Monitoring Checklist

* [x] Django/Gunicorn logs reviewed
* [x] Nginx logs reviewed
* [x] Celery logs reviewed
* [x] PostgreSQL logs reviewed
* [x] Redis logs reviewed
* [x] Django health endpoint available
* [x] PostgreSQL health endpoint available
* [x] Redis health endpoint available
* [x] Sensitive information excluded from health responses
* [x] Troubleshooting procedure documented
