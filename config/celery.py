import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = "Europe/Moscow"
app.conf.enable_utc = False

app.conf.beat_schedule = {
    "check-inactive-users-every-day": {
        "task": "habit.tasks.check_inactive_users",
        "schedule": crontab(hour=0, minute=0),
    },
}

app.autodiscover_tasks()
