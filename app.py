from flask import Flask
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import register_routes
    register_routes(app)

    return app
