from os import path, getenv
import uuid


class Config(object):
    basedir = path.abspath(path.dirname(__file__))

    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        getenv('DB_ENGINE', 'postgresql'),
        getenv('DB_USERNAME', 'admin'),
        getenv('DB_PASS', 'qwerty'),
        getenv('DB_HOST', 'localhost'),
        getenv('DB_PORT', 5439),
        getenv('DB_NAME', 'scrum-board-db')
    )

    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', uuid.uuid4().hex)
    print(SQLALCHEMY_DATABASE_URI)
    print(JWT_SECRET_KEY)
