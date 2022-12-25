from importlib import import_module
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from apps.auth.routes import auth_blueprint
db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in {'auth'}:
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config)
    register_extensions(app)

    register_blueprints(app)
    configure_database(app)
    Migrate(app, db)
    JWTManager(app)
    # configure_database(app)
    return app
