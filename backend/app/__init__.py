from flask import Flask
from flasgger import Swagger

from app.config import BaseConfig, TestConfig
from app.api.dependencies import db
from app.swagger import template, swagger_config
from app.api.users import users
from app.api.groups import groups
from app.api.members import members


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SWAGGER={
            'title': 'Flask React API',
            'uiversion': 3
        }
    )

    if test_config is None:
        app.config.from_object(BaseConfig)
    else:
        app.config.from_object(test_config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    Swagger(app, config=swagger_config, template=template)

    app.register_blueprint(users)
    app.register_blueprint(groups)
    app.register_blueprint(members)

    return app
