from app import create_app
from celery import Celery

app = create_app()
celery = Celery(app.import_name, broker='redis://localhost:6379/0')  # Or RabbitMQ if used

celery.conf.update(app.config)
from celeryconfig import beat_schedule
celery.conf.beat_schedule = beat_schedule

# Bind Flask context to Celery tasks
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
