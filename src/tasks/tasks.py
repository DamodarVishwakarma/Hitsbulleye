"""
Celery worker tasks definition
"""
from celery.schedules import crontab
from src.tasks.celery import celery_master_app

celery_master_app.autodiscover_tasks()
celery_master_app.conf.timezone = "UTC"

celery_master_app.conf.beat_schedule = {

}
