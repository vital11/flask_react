template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask React API",
        "description": "API for Flask React test project",
        "contact": {
            "name": "Git",
            "url": "https://github.com/vital11/flask_react.git",
        },
        "version": "1.0.1"
    },
    "basePath": "/",
    "schemes": [
        "http",
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. "
                           "Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
}
