from backend.app import create_app
from backend.routes.tasks import daily_appointment_reminder

app = create_app()
with app.app_context():
    daily_appointment_reminder.delay()
    print(" Email sent! Check Gmail!")