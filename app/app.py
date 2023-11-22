from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    from . import models, views
    db.init_app(app)
    app.register_blueprint(views.bp)

    return app

