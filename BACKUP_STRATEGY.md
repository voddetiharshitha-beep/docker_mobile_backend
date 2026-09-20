# Backup Strategy

## 1. What is backed up?

The PostgreSQL database is the primary persistent data source for the Django backend.

The database contains application data such as users, authentication data, tasks, and other relational records.

## 2. Backup method

PostgreSQL backups are created using `pg_dump`.

Example:

```powershell
docker compose exec postgres pg_dump -U django_user -d django_db > backup.sql