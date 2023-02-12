import os

from flask import Flask
from flasgger import Swagger

import app.settings
from app.api.users import users
from app.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        SQLALCHEMY_DATABASE_URL=settings.SQLALCHEMY_DATABASE_URL,
        SWAGGER={
            'title': 'Flask React API',
            'uiversion': 3
        }
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Swagger(app, config=swagger_config, template=template)

    return app
