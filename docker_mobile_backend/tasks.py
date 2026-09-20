from celery import shared_task
from django.db import connection


@shared_task
def test_celery_database_task():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]

    return f"Celery connected to PostgreSQL successfully: {result}"