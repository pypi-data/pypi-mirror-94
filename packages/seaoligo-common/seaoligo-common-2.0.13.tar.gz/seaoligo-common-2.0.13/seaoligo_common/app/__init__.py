import os
import pathlib
import json
from flask import Flask, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from seaoligo_common.config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    Create a Flask application using the app factory pattern.

    :param config_name: Setup app configuration.
    :return: Flask app
    """
    if not os.environ.get('SECRET_KEY'):
        raise NameError('SECRET_KEY must be defined!')  # pragma: no cover

    if not os.environ.get('PG_PASSWORD'):
        raise NameError('PG_PASSWORD must be defined!')  # pragma: no cover

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.from_pyfile('local_settings.py', silent=True)

    db.init_app(app)

    @app.before_request
    def current_user():
        payload = request.headers.get('Current-User')
        g.current_user = json.loads(payload) if payload else None

    @app.after_request
    def add_header(response):
        server_id = pathlib.Path(os.getcwd()).parts[-1]
        response.headers['Server-Id'] = server_id

        return response

    @app.route('/')
    def index():
        server_id = pathlib.Path(os.getcwd()).parts[-1]
        response = jsonify({'message': f'{server_id} service is up!'})

        return response

    return app
