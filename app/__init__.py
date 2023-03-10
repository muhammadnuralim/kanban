from flask import Flask
from jinja2 import TemplateNotFound
from config import config
from flask_jwt_extended import JWTManager
import os



def create_app():
    app = Flask(__name__)
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DEV_DATABASE_URL")
    app.config["SECRET_KEY"] = 'dev'
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    from app.login import auth
    app.register_blueprint(auth)
    from app.home import admin
    app.register_blueprint(admin, url_prefix="/admin")

    jwt = JWTManager(app)

    config[config_name].init_app(app)
    print(app.url_map)
    # app.register_blueprint(pages, url_prefix="/home")

    from app.model import db
    db.init_app(app)       
    with app.app_context():
        db.create_all()
    return app