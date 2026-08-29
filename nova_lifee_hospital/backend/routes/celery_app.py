from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "hms_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["backend.routes.tasks"]   
)

def init_celery(app):
    celery.conf.update(app.config)

    celery.conf.enable_utc = False
    celery.conf.timezone = "Asia/Kolkata"

    celery.conf.beat_schedule = {
        "daily-appointment-reminder": {
            "task": "backend.routes.tasks.daily_appointment_reminder",   
            "schedule": crontab(hour=8, minute=0),
        },
        "monthly-doctor-report": {
            "task": "backend.routes.tasks.monthly_doctor_report",   
            "schedule": crontab(day_of_month=1, hour=9, minute=0),
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery