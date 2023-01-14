from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = "wsgi.py"

    # app.config['UPLOAD_FOLDER'] = '\models\data'
# app.secret_key = "Khaif"
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Flask-Assets
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = True
    LESS_RUN_IN_DEBUG = True

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = True

    # Datadog
    DD_SERVICE = environ.get("DD_SERVICE")
    UPLOAD_FOLDER = '\models\data'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # API
    BEST_BUY_API_KEY = environ.get("BEST_BUY_API_KEY")