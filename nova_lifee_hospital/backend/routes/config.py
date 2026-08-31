import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Render pe DATABASE_URL milega (Postgres), local pe nahi milega (SQLite fallback)
    _db_url = os.getenv("DATABASE_URL")
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url or ("sqlite:///" + os.path.join(BASE_DIR, "hms.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "afroz.sum17@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "okosjxnglfquedjh")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME", "afroz.sum17@gmail.com")