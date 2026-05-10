import os

from flask import Flask
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    database_uri = app.config['DATABASE_URI']
    if database_uri.startswith('libsql://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+libsql://' + database_uri[len('libsql://'):]
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {'auth_token': os.environ.get('TURSO_AUTH_TOKEN', '')}
        }
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import register_routes
    register_routes(app)

    return app
