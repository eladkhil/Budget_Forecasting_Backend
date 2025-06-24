from celery.schedules import crontab

beat_schedule = {
    "send-password-expiry-emails": {
        "task": "app.tasks.reminders.send_expiry_warnings",
        "schedule": crontab(hour=8, minute=0),  # Every day at 8 AM
    },
}
