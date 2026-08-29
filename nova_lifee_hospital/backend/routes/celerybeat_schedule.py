from celery.schedules import crontab

beat_schedule = {
    "daily-reminder": {
        "task": "backend.routes.tasks.daily_appointment_reminder",
        "schedule": crontab(hour=8, minute=0),   
    },


    "monthly-doctor-report": {
        "task": "backend.routes.tasks.monthly_doctor_report", 
        "schedule": crontab(day_of_month=1, hour=8, minute=0),
    }
}
