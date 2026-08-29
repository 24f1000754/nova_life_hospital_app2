#celery_worker.py
from backend.app import create_app
from backend.routes.celery_app import celery, init_celery

#vreating flask app
flask_app = create_app()

#giving flask context to celery
init_celery(flask_app)
from backend.routes import tasks