from flask import Flask
from backend.routes.config import Config
from backend.models.models import db
from backend.routes.auth import auth_bp, create_default_admin
from backend.routes.doctor import doctor_bp
from backend.routes.appointment import appointment_bp
from flask_cors import CORS
# from admin import admin_bp
from backend.routes.admin import admin_bp
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    #i initialized my database here
    db.init_app(app)
    
    #i initialize mail here
    mail.init_app(app)

    # blueprints register
    app.register_blueprint(auth_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return {"status": "HMS MAD-2 project backend running "}

     
    with app.app_context():
        db.create_all()
        create_default_admin()
        print(" Database tables created")

    # celery initializing for ingnoring circular import
    from backend.routes.celery_app import init_celery
    init_celery(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)