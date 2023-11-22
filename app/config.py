import os

class Config:
    DEBUG = False
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///gestion.db"

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_APP = "mi_app.app:create_app('mi_app.config.DevelopmentConfig')"
    FLASK_ENV = "development"

class ProductionConfig(Config):
    DEBUG = False
    FLASK_APP = "mi_app.app:create_app('mi_app.config.ProductionConfig')"
    FLASK_ENV = "production"
